from ._tables import TaskRecord
from ._base import BaseRepo

from sqlalchemy import select

from ...schema.enum import PullDataFormatEnum


class TaskRecordRepo(BaseRepo):

    def __init__(self, task_id):
        self.t: TaskRecord = TaskRecord.instance(task_id=task_id)

    def create_tabel(self):
        self.t.create()

    def is_exist(self):
        return self.t.is_exists()

    def select_by_id(self, row_id: int):
        stmt = (select(self.t.task_name,
                       self.t.task_type)
                .where(self.t.id == row_id))
        return self.execute(stmt, output=PullDataFormatEnum.RECORDS)
