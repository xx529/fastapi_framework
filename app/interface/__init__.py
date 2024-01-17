from .repo.user_repo import UserInfoRepo
from .repo.task_repo import TaskRecordRepo
from .cache.redis import Redis
from app.config import redis_conf

redis = Redis(conf=redis_conf)
