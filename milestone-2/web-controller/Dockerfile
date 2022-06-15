# FROM python:3.5.1-onbuild
FROM python:3.7-alpine

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]