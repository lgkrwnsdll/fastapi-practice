from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config.db_config import session_context
from app.config.settings import settings

SYNC_URL = f"mysql+pymysql://{settings.db_username}:{settings.db_password}@localhost:3306/ddtesttest"
test_engine = create_engine(
    SYNC_URL,
    pool_size=5,
    # echo=True,
    # echo_pool="debug",
)

ASYNC_URL = f"mysql+aiomysql://{settings.db_username}:{settings.db_password}@localhost:3306/ddtesttest"
test_async_engine = create_async_engine(
    ASYNC_URL,
    pool_size=40,
    # echo=True,
    # echo_pool="debug",
)
test_async_session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=test_async_engine)


async def override_inject_session():
    """
    AsyncClient와 FastAPI 앱을 활용한 테스트에서 적용 가능
    중첩 트랜잭션을 사용해 테스트 내에서 커밋이 일어나도 외부 트랜잭션의 롤백으로 초기화
    
    하나의 요청에서 두 개 이상의 독립된 트랜잭션을 활용하는 경우는 이 세션으로 테스트 불가
    """
    async with test_async_engine.connect() as conn:
        async with conn.begin() as trans:
            session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint")
            token = session_context.set(session)
            yield session

            await trans.rollback()

    await test_async_engine.dispose()  # 생략 시 여러 테스트를 실행하면 event loop 관련 에러 발생
    session_context.reset(token)

