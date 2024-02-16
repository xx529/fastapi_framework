from app.schema.task import TaskCategory, TaskID, TaskName
from app.schema.user import UserID

from sqlalchemy.ext.asyncio import AsyncSession


class TaskService:

    def __init__(self, db: AsyncSession = None):
        self.db = db

    def create_task(self, task_name: TaskName, category: TaskCategory, user_id: UserID) -> TaskID:
        print(self)
        return 1
