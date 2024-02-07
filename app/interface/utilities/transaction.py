from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.apiserver.logger import transaction_log
from ..repo._base import AsyncSessionLocal, SessionLocal


class DataBaseTransaction:

    def __init__(self):
        self.db: Session = None

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
            self.db.commit()
            self.db.close()
            transaction_log.debug('close transaction')


class AsyncDataBaseTransaction:

    def __init__(self, commit=True):
        self.db: AsyncSession = None
        self.commit = commit

    async def __aenter__(self):
        transaction_log.debug('create async transaction')
        self.db = AsyncSessionLocal()
        return self.db

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.db.rollback()
            await self.db.close()
            transaction_log.error(f'transaction error: {str(exc_val)}')
            raise exc_val
        else:
            if self.commit:
                await self.db.commit()
            await self.db.close()
            transaction_log.debug('close async transaction')
