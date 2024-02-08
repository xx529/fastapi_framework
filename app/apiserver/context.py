from uuid import UUID
import contextvars

request_id = contextvars.ContextVar('request_id')


class RequestCtx:

    @staticmethod
    def get_request_id() -> str | None:
        try:
            return request_id.get()
        except Exception:
            return None

    @staticmethod
    def set_request_id(value: UUID):
        request_id.set(value.hex)
