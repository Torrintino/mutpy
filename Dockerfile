FROM python:3.7-slim

COPY requirements.txt /home/app/opt/app/requirements.txt

WORKDIR /home/app

RUN pip install -r /home/app/opt/app/requirements.txt

ENV PYTHONPATH=/home/app

COPY . .

CMD ["python3","-u", "/home/app/bin/mut.py"]
