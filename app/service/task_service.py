from app.schema.task import TaskCategory, TaskID, TaskName
from app.schema.user import UserID


class TaskService:

    @staticmethod
    def create_task(task_name: TaskName, category: TaskCategory, user_id: UserID) -> TaskID:
        return 1
