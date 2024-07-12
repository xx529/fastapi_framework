from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)


print(User(id=1, name='a'))
print(User(id=1, name='a').model_dump())
