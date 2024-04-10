import contextvars
import uuid

trace_id_var = contextvars.ContextVar('trace_id')
step_num_var = contextvars.ContextVar('step_num')


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


class LoggerStep:

    @staticmethod
    def get_step_num() -> int:
        try:
            LoggerStep.add()
            return step_num_var.get()
        except Exception:
            return None

    @staticmethod
    def add():
        num = step_num_var.get() + 1
        step_num_var.set(num)

    @staticmethod
    def reset_step_num():
        step_num_var.set(0)
