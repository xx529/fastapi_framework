from sqlalchemy.ext.asyncio import AsyncSession

from app.interface import AsyncDataBaseTransaction
from app.interface.repo.task_repo import TaskInfoRepo, TaskRecordRepo


class TaskService:

    def __init__(self, db: AsyncSession = None):
        self.db = db

    @staticmethod
    async def create_task(name, category, user_id) -> int:
        async with AsyncDataBaseTransaction() as db:
            task_id = await TaskInfoRepo(db=db).create(name=name,
                                                       category=category,
                                                       user_id=user_id)
            TaskRecordRepo(db=db, task_id=task_id).create_table()
        return task_id
