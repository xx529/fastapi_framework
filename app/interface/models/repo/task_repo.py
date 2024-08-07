from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.interface.models.base import BaseRepo
from app.interface.models.tables import TaskInfo, TaskRecord
from app.schema.const import TaskStatus


class TaskInfoRepo(BaseRepo):

    def __init__(self, db: AsyncSession):
        self.model: TaskInfo = TaskInfo.instance()
        self.db = db

    async def create(self, name: str, category: str, user_id: int):
        sql = (insert(self.model)
               .values(name=name,
                       category=category,
                       user_id=user_id,
                       status=TaskStatus.ON.value,
                       del_flag=False)
               .returning(self.model.id))
        data = await self.aexec(sql, output='raw')
        task_id = data.first()
        return task_id

    async def delete_task(self, task_id: int):
        sql = (update(self.model)
               .where(self.model.id == task_id)
               .values(del_flag=True))
        await self.aexec(sql, output=None)


class TaskRecordRepo(BaseRepo):

    def __init__(self, db: AsyncSession, task_id):
        self.model: TaskRecord = TaskRecord.instance(task_id=task_id)
        self.db = db

    def select_by_id(self, row_id: int):
        stmt = (select(self.model.name,
                       self.model.category)
                .where(self.model.id == row_id))
        return self.exec(stmt, output='list')
