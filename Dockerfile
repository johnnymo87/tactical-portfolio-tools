FROM python:3.10-bullseye

WORKDIR /app
ENV PYTHONPATH=.
COPY requirements.txt .
RUN  pip install --upgrade pip && \
     pip install pip-tools && \
     pip install -r requirements.txt

COPY . /app

RUN ln -sf /app/.python_history ~/.python_history

CMD python .
