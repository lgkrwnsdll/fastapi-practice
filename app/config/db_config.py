from contextvars import ContextVar

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config.settings import settings

ASYNC_URL = f"mysql+aiomysql://{settings.db_username}:{settings.db_password}@localhost:3306/ddtest"
async_engine = create_async_engine(
    ASYNC_URL,
    pool_size=40,
    echo=True,
    echo_pool="debug",
)
# 의존성 주입을 잘 활용하면 scoped_session 없이도 요청 별 트랜잭션 처리가 가능할 뿐 아니라 테스트 코드 설정이 더 용이해진다
async_session_factory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False
)

# Transactional 데코레이터를 프로덕션, 테스트 코드에서 모두 원활하게 사용할 수 있게 해주는 세션 컨텍스트 관리자
session_context: ContextVar[AsyncSession] = ContextVar("session_context")


async def inject_session():
    """
    같은 요청 컨텍스트 내에서는 최초 호출 이후 캐시된 세션 반환
    라우터 메서드 반환 이후 yield 다음의 로직 수행

    DB 작업이 없는 API에서는 DB 커넥션을 얻어오지 않아 효율적
    """
    session = async_session_factory()
    token = session_context.set(session)
    try:
        yield session
    finally:
        await session.close()
        session_context.reset(token)
