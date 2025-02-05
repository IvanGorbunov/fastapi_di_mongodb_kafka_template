FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP__HOME_DIR=/home
ENV PYTHONPATH=/home/src


RUN apt update -y && \
    apt install --no-install-recommends -y \
        libpython3-dev \
        libpq-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR $APP__HOME_DIR
COPY . .

RUN poetry install --no-root

COPY ./entrypoint-web.sh $APP__HOME_DIR/entrypoint-web.sh

RUN chmod +x $APP__HOME_DIR/entrypoint-web.sh
