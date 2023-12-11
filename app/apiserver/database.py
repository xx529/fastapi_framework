from typing import Dict

from sqlalchemy import BIGINT, Boolean, Column, DateTime, func, String
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import PgDataBaseConf

engine = PgDataBaseConf.engine

inspector = Inspector.from_engine(engine)
Base = declarative_base()


class BaseTableAttr(Base):
    TABLE_NAME: str = None
    SCHEMA: str = None
    ENGINE: Engine = None

    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': PgDataBaseConf.schema}

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment="唯一ID值")
    create_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    create_by = Column(String(64), index=False, nullable=False, comment="创建者")
    update_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="最后更新时间")
    update_by = Column(String(64), index=False, comment="最后更新者")
    del_flag = Column(Boolean, index=False, default=False, nullable=False, comment="安全删除标记")

    @classmethod
    def create(cls):
        cls.__table__.create(bind=cls.engine)

    @classmethod
    def is_exists(cls):
        return Inspector.from_engine(cls.engine).has_table(cls.__tablename__)


class SingletonTable(BaseTableAttr):
    __abstract__ = True
    __tablename__: str


class MultipleTable(BaseTableAttr):
    __abstract__ = True
    __tablename__: str
    __basename__: str
    instances: Dict[str, Base] = {}

    @classmethod
    def get_instance(cls, prefix=None, suffix=None) -> "MultipleTable":
        table_name = cls.__basename__
        if prefix:
            table_name = f'{prefix}_{table_name}'
        if suffix:
            table_name = f'{table_name}_{suffix}'

        if table_name not in cls.instances:
            print(f'create instance class: {table_name}')
            instance = type(table_name, (Base, cls), {'__tablename__': table_name})
            cls.instances[table_name] = instance
        else:
            print(f'exist instance class: {table_name}')
        return cls.instances[table_name]


SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_session(function):
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        result = function(db, *args, **kwargs)
        db.close()
        return result

    return wrapper
