FROM python:3.11

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY app /app

CMD ["poetry", "run", "uvicorn", "app.main:myapp"]
