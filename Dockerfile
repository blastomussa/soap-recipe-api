FROM python:3.10.7-slim-bullseye

ENV DOCKER_IMG=true

WORKDIR /API

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 80

WORKDIR /API/app

RUN pip freeze

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80