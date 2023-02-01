FROM python:3.10.0-slim
RUN apt-get update \
    && apt-get install g++ -y \
    && apt-get clean

# Configure Poetry
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PROCESS_RUN_TIMEOUT_SECONDS=15

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install

# should ensure that empty directories are copied too - for the cpp-source-files directory
COPY . /app

HEALTHCHECK CMD poetry run healthcheck

ENTRYPOINT poetry run python main.py