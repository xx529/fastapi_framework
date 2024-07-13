from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    create_at: datetime = Field(max_length=100)
    create_by: int = Field(max_length=100)
    update_at: datetime = Field(max_length=100)
    update_by: int = Field(max_length=100)
    deleted_at: datetime = Field(max_length=100)
    deleted_by: int = Field(default=False)


class User(BaseModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)


print(User(id=1, name='a'))
print(User(id=1, name='a').model_dump())
