from functools import wraps

from app.config.db_config import session_context


class Transactional:
    def __init__(self, read_only=False):
        """트랜잭션의 범위를 최소화 하기 위해 읽기 작업에도 사용"""
        self.read_only = read_only

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            session = session_context.get()  # 세션 주입 시 ContextVar에 저장한 AsyncSession 인스턴스
            try:
                result = await func(*args, **kwargs)

                if not self.read_only:
                    await session.commit()  # 하나 이상의 repository 작업을 하나의 트랜잭션으로 커밋
            except Exception as e:
                if not self.read_only:
                    await session.rollback()
                raise e
            finally:
                await session.close()

            return result

        return wrapper


# 요청마다 고유한 세션 객체가 배정되어야하는데, 싱글톤 적용 시 순차적인 요청에서 같은 세션 사용되며 커넥션 풀에 반환되지 않음
class Singleton:
    __instances = {}

    def __init__(self, cls):
        self.cls = cls
        wraps(self.cls)(self)

    def __call__(self, *args, **kwargs):
        if self.cls not in self.__instances:
            self.__instances[self.cls] = self.cls(*args, **kwargs)
        return self.__instances[self.cls]
