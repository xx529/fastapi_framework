from sqlalchemy.ext.asyncio import AsyncSession

from app.interface import AsyncDataBaseTransaction
from app.interface.repo.task_repo import TaskInfoRepo, TaskRecordRepo
from app.schema.task import TaskCreateRequestBody


class TaskService:

    def __init__(self, db: AsyncSession = None):
        self.db = db

    @staticmethod
    async def create_task(body: TaskCreateRequestBody) -> int:
        async with AsyncDataBaseTransaction() as db:
            task_id = await TaskInfoRepo(db=db).create(name=body.name,
                                                       category=body.category.value,
                                                       user_id=body.user_id)
            TaskRecordRepo(db=db, task_id=task_id).create_table()
        return task_id
