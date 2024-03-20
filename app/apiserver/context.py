import contextvars
import uuid
from uuid import UUID

request_id = contextvars.ContextVar('request_id')



class RequestCtx:

    @staticmethod
    def get_trace_id() -> str | None:
        try:
            return request_id.get()
        except Exception:
            return None

    @staticmethod
    def set_trace_id(value: UUID):
        request_id.set(value.hex)

    @staticmethod
    def create_trace_id() -> UUID:
        return uuid.uuid4()
