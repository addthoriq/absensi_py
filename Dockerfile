FROM python:3.12
LABEL version="1.0.0"
LABEL maintainer="thoriq@qti.co.id"

WORKDIR /usr/src/app
ENV DEBIAN_FRONTEND='noninteractive'
RUN apt-get update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml ./
COPY poetry.lock ./
COPY . .
RUN poetry install
EXPOSE 8000
RUN poetry run alembic upgrade head
