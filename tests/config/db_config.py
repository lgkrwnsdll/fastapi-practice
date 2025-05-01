from sqlalchemy import create_engine, NullPool
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
    # pool_size=40,
    poolclass=NullPool,
    # echo=True,
    # echo_pool="debug",
)
test_async_session_factory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_async_engine,
    expire_on_commit=False
)


async def override_inject_session():
    """
    AsyncClient와 FastAPI 앱을 활용한 테스트에서 적용 가능

    중첩 트랜잭션을 사용해 테스트 내에서 커밋이 일어나도 외부 트랜잭션의 롤백으로 초기화

    엔진이 여러 이벤트 루프에서 사용되는 경우, 기본 엔진 설정으로는 재사용되기 전 dispose() 처리가 되어야한다.
    혹은 커넥션 풀을 사용하지 않아 dispose 할 필요가 없도록 NullPool을 설정해야 한다.
    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
    """
    async with test_async_engine.connect() as conn:
        async with conn.begin() as trans:
            session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint")
            token = session_context.set(session)
            yield session

            await trans.rollback()

    session_context.reset(token)

