from sqlalchemy import Column, String
from app.apiserver.database import TableFactory


class TaskRecord(TableFactory):
    __basename__ = 'task'

    task_name = Column(String(255), nullable=False, comment='任务名称')


class TaskRecordRepo:

    def __init__(self, task_id):
        self.table = TaskRecord.instance(suffix=task_id)
        self.db = None

    def create_tabel(self):
        self.table.create()


table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)


