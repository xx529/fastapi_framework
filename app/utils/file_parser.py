class BaseMarkdownParser:

    def load(self) -> str:
        raise NotImplementedError


class WORD2MarkdownLoader(BaseMarkdownParser):
    ...


class PPT2MarkdownLoader(BaseMarkdownParser):
    ...


class EXCELLoader:
    ...
