FROM python:3.7-slim

COPY requirements.txt /app/requirements.txt

WORKDIR app

RUN pip install -r /app/requirements.txt

ENV PYTHONPATH=/app

COPY . .

CMD ["python3","-u", "/app/bin/mut.py"]
