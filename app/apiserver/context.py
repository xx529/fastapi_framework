import contextvars
import uuid

from pydantic import BaseModel, Field

trace_id_var = contextvars.ContextVar('trace_id')
ctx_var = contextvars.ContextVar('ctx')


class ContextInfo(BaseModel):
    trace_id: str | None = Field(None, description='日志追踪ID')
    user_id: int | None = Field(None, description='用户ID')


class RunContext:

    def __init__(self, ctx: ContextInfo):
        self.ctx = ctx
        self.token = None

    def __enter__(self):
        self.token = ctx_var.set(self.ctx.model_copy(deep=True))
        return self.ctx

    def __exit__(self, exc_type, exc_val, exc_tb):
        ctx_var.reset(self.token)
        if exc_type:
            raise exc_val

    @classmethod
    def update(cls, **kwargs):
        new_ctx = cls.current().copy(update=kwargs)
        return cls(ctx=new_ctx)

    @classmethod
    def current(cls) -> ContextInfo | None:
        try:
            return ctx_var.get()
        except Exception as _:
            return ContextInfo()


class RequestCtx:

    @staticmethod
    def get_trace_id() -> str | None:
        try:
            return trace_id_var.get()
        except Exception:
            return None

    @staticmethod
    def create_trace_id() -> str:
        trace_id = uuid.uuid4().hex
        trace_id_var.set(trace_id)
        return trace_id

    @staticmethod
    def set_trace_id(trace_id) -> None:
        trace_id_var.set(trace_id)


if __name__ == '__main__':
    t1 = ContextInfo(trace_id='a', user_id=1)
    print(RunContext.current())

    with RunContext(ctx=t1):
        print(RunContext.current())

        with RunContext.update(trace_id='bbb'):
            print(RunContext.current())

            with RunContext.update(user_id=999):
                print(RunContext.current())

            print(RunContext.current())

        print(RunContext.current())

    print(RunContext.current())
