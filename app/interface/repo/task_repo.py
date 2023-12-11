from sqlalchemy import Column, String

from app.apiserver.database import MultipleTable


class TaskRecord(MultipleTable):
    __abstract__ = True
    __basename__ = 'task'

    task_name = Column(String(255), nullable=False, comment='任务名称')


class TaskRecordRepo:

    def __init__(self, task_id):
        self.t = TaskRecord.get_instance(suffix=task_id)
        self.db = None

    def create_tabel(self):
        print(f'create table: {self.t.__tablename__}')
        self.t.create()
        return self
