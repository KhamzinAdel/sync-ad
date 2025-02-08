FROM python:3.10.0-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry==1.3.2 && poetry settings virtualenvs.create false

WORKDIR /app/

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install
COPY . .

EXPOSE 8000