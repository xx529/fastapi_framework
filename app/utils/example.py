from app.schema.base import Example, ExampleSet
from app.schema.schemas.user import UserCreateBody

user_create_examples = ExampleSet(examples=[
    Example(
        summary='例子1（适用于开发环境）',
        description='一般例子1',
        value=UserCreateBody(name='张三', age=30, gender='男')
    ),
    Example(
        summary='例子2',
        description='一般例子2',
        value=UserCreateBody(name='张三', age=28, gender='女')
    )
]).to_openapi_examples()
