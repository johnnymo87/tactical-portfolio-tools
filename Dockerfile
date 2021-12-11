FROM python:3.10-bullseye AS production

WORKDIR /app
ENV PYTHONPATH=.
COPY requirements.txt .
RUN  pip install --upgrade pip && \
     pip install pip-tools && \
     pip-sync

COPY . /app

CMD python .

FROM production AS development

RUN pip-sync requirements.txt dev-requirements.txt
RUN ln -sf /app/.python_history ~/.python_history
