from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.apiserver.logger import transaction_log
from ..models import AsyncSessionLocal, SessionLocal


class DataBaseTransaction:

    def __init__(self, commit: bool = True):
        self.commit: bool = commit
        self.db: Session | None = None
        self.adb: AsyncSession | None = None

    def __enter__(self):
        transaction_log.debug('create transaction')
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
            self.db.close()
            transaction_log.error(f'transaction error: {str(exc_val)}')
            raise exc_val
        else:
            if self.commit:
                self.db.commit()
            self.db.close()
            transaction_log.debug('close transaction')

    async def __aenter__(self):
        transaction_log.debug('create async transaction')
        self.adb = AsyncSessionLocal()
        return self.adb

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.adb.rollback()
            await self.adb.close()
            transaction_log.error(f'transaction error: {str(exc_val)}')
            raise exc_val
        else:
            if self.commit:
                await self.adb.commit()
            await self.adb.close()
            transaction_log.debug('close async transaction')
