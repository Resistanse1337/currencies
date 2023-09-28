ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION} as python

WORKDIR /currencies

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update --fix-missing && apt-get install --no-install-recommends -y build-essential libpq-dev

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000