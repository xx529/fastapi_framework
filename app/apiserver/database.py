from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BIGINT, DateTime, Column, String, func, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DataBaseConf
from typing import Dict, Any, Union


Base = declarative_base()

engine = create_engine(url=DataBaseConf.jdbcurl,
                       connect_args={},
                       pool_pre_ping=True,
                       pool_recycle=1200)


class BaseTableAttr:
    __allow_unmapped__ = True
    __table_args__ = {'schema': DataBaseConf.schema}

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment="唯一ID值")
    create_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    create_by = Column(String(64), index=False, nullable=False, comment="创建者")
    update_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="最后更新时间")
    update_by = Column(String(64), index=False, comment="最后更新者")
    del_flag = Column(Boolean, index=False, default=False, nullable=False, comment="安全删除标记")


class SingletonTable(Base, BaseTableAttr):
    __abstract__ = True
    __tablename__: str


class MultipleTable(BaseTableAttr):
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

    @classmethod
    def create(cls):
        getattr(cls, '__table__').create(bind=engine)


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
