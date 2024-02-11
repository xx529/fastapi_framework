from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ._base import BaseRepo
from ._tables import TaskRecord


class TaskRecordRepo(BaseRepo):

    def __init__(self, db: AsyncSession, task_id):
        self.model: TaskRecord = TaskRecord.instance(task_id=task_id)
        self.db = db

    def create_tabel(self):
        self.model.create()

    def is_exist(self):
        return self.model.is_exists()

    def select_by_id(self, row_id: int):
        stmt = (select(self.model.task_name,
                       self.model.catgory)
                .where(self.model.id == row_id))
        return self.exec(stmt, output='list')
