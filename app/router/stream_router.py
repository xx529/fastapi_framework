from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.service.stream_service import StreamService

router = APIRouter(prefix='/stream', tags=['流式接口模块'])


@router.get(path='/stream')
async def stream():
    generator = StreamService.demo()
    return StreamingResponse(generator, media_type="text/event-stream")
