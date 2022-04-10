FROM python:3.10-bullseye AS production

WORKDIR /app
ENV PYTHONPATH=.
ENV POETRY_HOME=/usr/local
COPY poetry.lock pyproject.toml ./
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry install --no-dev

COPY . /app

CMD poetry run python .

FROM production AS development

RUN poetry install && \
    ln -sf /app/.python_history ~/.python_history
