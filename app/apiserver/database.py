from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BIGINT, DateTime, Column, String, func, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DataBaseConf

Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': DataBaseConf.schema}

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment="唯一ID值")
    create_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    create_by = Column(String(64), index=False, nullable=False, comment="创建者")
    update_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="最后更新时间")
    update_by = Column(String(64), index=False, comment="最后更新者")
    del_flag = Column(Boolean, index=False, default=False, nullable=False, comment="安全删除标记")


engine = create_engine(url=DataBaseConf.jdbcurl,
                       connect_args={},
                       pool_pre_ping=True,
                       pool_recycle=1200)

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
