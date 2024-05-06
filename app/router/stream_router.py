import asyncio

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse

from app.schema.base import OkResponse, StrResponse
from app.service.stream_service import StreamService

router = APIRouter(prefix='/stream', tags=['流式接口模块'])

data = []


async def add_data():
    async def func():
        n = 0
        while True:
            await asyncio.sleep(0.5)
            if len(data) >= 20:
                break
            else:
                n += 1
                print(len(data), n)
                data.append(n)

    await asyncio.create_task(func())


def get():
    async def g():
        while True:
            if len(data) == 0:
                await asyncio.sleep(1)
            else:
                n = data.pop()
                print(f'get: {n}')
                yield str(n) + '\n\n'

    return g()


@router.get(path='/stream')
async def stream():
    generator = StreamService.demo()
    return StreamingResponse(generator, media_type="text/event-stream")


@router.get(path='/stream/queue')
def queue_stream():
    generator = get()
    print(type(generator))
    return StreamingResponse(generator, media_type="text/event-stream")


@router.post(path='/queue', response_model=OkResponse)
async def queue_post(background_tasks: BackgroundTasks):
    background_tasks.add_task(add_data)
    return OkResponse(data='ok')


@router.get(path='/queue', response_model=StrResponse)
async def queue_get():
    return StrResponse(data=str(len(data)))
