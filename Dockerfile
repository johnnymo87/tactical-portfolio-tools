# Base image
FROM python:3.8.3-buster AS base

COPY requirements.txt /tmp/requirements.txt
RUN  pip3 install -r /tmp/requirements.txt

# Release image
FROM base AS release

WORKDIR /app
COPY . /app
ENV PYTHONPATH=.

CMD python3 .

# Test image
FROM release AS test

RUN ln -sf /app/.python_history ~/.python_history

CMD pytest
