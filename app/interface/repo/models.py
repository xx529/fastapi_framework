from datetime import datetime

from sqlmodel import Field, SQLModel


class StrId(SQLModel):
    id: str = Field(primary_key=True)


class IntId(SQLModel):
    id: int = Field(primary_key=True)


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    create_at: datetime = Field(default_factory=datetime.now, max_length=100)
    create_by: int = Field(max_length=100)
    update_at: datetime = Field(default_factory=datetime.now, max_length=100)
    update_by: int = Field(max_length=100)
    deleted_at: datetime = Field(max_length=100)
    deleted_by: int = Field(default=False)


class User(IntId, BaseModel, table=True):
    name: str = Field(max_length=100)


print(User(id=1, name='a'))
print(User(id=1, name='a').model_dump())
