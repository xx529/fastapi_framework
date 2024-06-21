FROM python:3.11

COPY app /app

CMD ["python3", "main.py"]
