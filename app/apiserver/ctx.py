import contextvars

request_id = contextvars.ContextVar('request_id')
