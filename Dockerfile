FROM python:3.11

RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    echo 'deb https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib' > /etc/apt/sources.list && \
    echo 'deb-src https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.aliyun.com/debian-security/ bookworm-security main' >> /etc/apt/sources.list && \
    echo 'deb-src https://mirrors.aliyun.com/debian-security/ bookworm-security main' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.aliyun.com/debian/ bookworm-updates main non-free non-free-firmware contrib' >> /etc/apt/sources.list && \
    echo 'deb-src https://mirrors.aliyun.com/debian/ bookworm-updates main non-free non-free-firmware contrib' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.aliyun.com/debian/ bookworm-backports main non-free non-free-firmware contrib' >> /etc/apt/sources.list && \
    echo 'deb-src https://mirrors.aliyun.com/debian/ bookworm-backports main non-free non-free-firmware contrib' >> /etc/apt/sources.list

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY app /app

CMD ["poetry", "run", "uvicorn", "app.main:myapp", "--port"]


