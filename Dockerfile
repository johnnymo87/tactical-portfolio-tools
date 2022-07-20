FROM python:3.10-bullseye AS production

WORKDIR /app
ENV PYTHONPATH=.
ENV POETRY_HOME=/usr/local
COPY poetry.lock pyproject.toml ./
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry install --no-dev

COPY beta_calculator/ beta_calculator/

CMD ["sleep", "infinity"]

FROM production AS development

COPY . ./

RUN poetry install && \
    ln -sf /app/.python_history ~/.python_history
