FROM python:alpine3.9

WORKDIR app
COPY Pipfile* /app/

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install

COPY . .
