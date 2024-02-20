import asyncio

from app.schema.schemas.stream import EndData, MiddleData, StartData


class StreamService:

    @staticmethod
    async def demo():
        await asyncio.sleep(1)
        yield StartData(data={'message': '开始'}).model_dump_json() + '\n\n'

        await asyncio.sleep(1)
        yield MiddleData(data={'message': '中间'}).model_dump_json() + '\n\n'

        await asyncio.sleep(1)
        yield EndData(data={'message': '结束'}).model_dump_json() + '\n\n'
