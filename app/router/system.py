from fastapi import APIRouter
from app.schema.base import RouterPrefix

router = APIRouter(prefix=f'/{RouterPrefix.system}', tags=[RouterPrefix.system])


@router.get('/health')
async def health():
    return 'ok'
