import io
from pathlib import Path


class MarkdownParser:

    def __init__(self, filepath_or_buffer: Path | io.BytesIO | bytes):
        self.file_or_buffer = filepath_or_buffer

    def load(self) -> str:
        raise NotImplementedError


class Word2MarkdownLoader(MarkdownParser):
    ...


class Ppt2MarkdownLoader(MarkdownParser):
    ...


class Pdf2MarkdownLoader(MarkdownParser):
    ...


class ExcelLoader:
    ...
