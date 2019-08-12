FROM python:3.7-slim

RUN apt-get update -qq && \
    # psql for `python manage.py dbshell` && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1

WORKDIR /app

RUN pip install pipenv
ADD Pipfile* /app/
RUN pipenv install
