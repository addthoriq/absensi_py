FROM python:3.12

LABEL version="1.0.0"
LABEL maintainer="thoriq@qti.co.id"

ENV DEBIAN_FRONTEND='noninteractive'

WORKDIR /usr/src/app

RUN apt-get update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:/root/.local/bin"
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml ./
COPY poetry.lock ./
COPY . .

RUN poetry install

COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
