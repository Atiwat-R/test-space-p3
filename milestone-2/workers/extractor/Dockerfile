FROM python:3.8-buster

RUN mkdir -p /test
WORKDIR /test

ADD ./requirements.txt /test/

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /test/

CMD ["python","extract.py"]