import contextvars

from pydantic import BaseModel, Field


class ContextInfo(BaseModel):
    trace_id: str | None = Field(None, description='日志追踪ID')
    user_id: int | None = Field(None, description='用户ID')


class RunContext:
    CTX_VAR = contextvars.ContextVar('ctx')

    def __init__(self, ctx: ContextInfo = None):
        self.ctx = ctx or ContextInfo()
        self.token = None

    def __enter__(self):
        self.token = self.CTX_VAR.set(self.ctx.model_copy(deep=True))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.CTX_VAR.reset(self.token)
        if exc_type:
            raise exc_val

    @classmethod
    def update(cls, **kwargs):
        new_ctx = cls.current().copy(update=kwargs)
        return cls(ctx=new_ctx)

    @classmethod
    def current(cls) -> ContextInfo | None:
        try:
            return cls.CTX_VAR.get()
        except Exception as _:
            return ContextInfo()


class DbSessionContext:
    SESSION_VAR = contextvars.ContextVar('db_session')

    def __init__(self, db_session):
        self.db_session = db_session
        ...

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db_session.commit()
        else:
            self.db_session.rollback()


if __name__ == '__main__':
    t1 = ContextInfo(trace_id='a', user_id=1)
    print(RunContext.current())

    with RunContext(ctx=t1) as r1:
        print(RunContext.current())

        with r1.update(trace_id='bbb') as r2:
            print(RunContext.current())

            with r2.update(user_id=999) as r3:
                print(RunContext.current())

            print(RunContext.current())

        print(RunContext.current())

    print(RunContext.current())
