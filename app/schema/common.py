from typing import Any, List

from pydantic import BaseModel, Field

from app.apiserver.context import RunContext
from app.schema.const import KafkaTopic


class Example(BaseModel):
    summary: str = Field(description='摘要')
    description: str = Field(description='描述')
    data: BaseModel = Field(description='值')

    def to_openapi(self):
        return {'summary': self.summary, 'description': self.description, 'value': self.data.model_dump(mode='json')}


class ExampleSet(BaseModel):
    examples: List[Example] = Field(description='OpenAPI示例')

    def to_openapi_examples(self):
        return {example.summary: example.to_openapi() for example in self.examples}


class KafkaMessage(BaseModel):
    trace_id: str | None = Field(RunContext.current().trace_id, description='来自的追踪ID')
    topic: KafkaTopic = Field(description='消息主题')
    data: Any = Field(description='消息内容')
