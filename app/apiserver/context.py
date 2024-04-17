import contextvars
import uuid

trace_id_var = contextvars.ContextVar('trace_id')


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
