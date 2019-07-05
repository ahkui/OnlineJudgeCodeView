FROM python:3-alpine

COPY . /app

WORKDIR /app

RUN apk add --no-cache build-base gcc make

RUN python -V

RUN python -m pip install setuptools django numpy

CMD python3 manage.py runserver 0.0.0.0:80
