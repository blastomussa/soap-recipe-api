FROM python:3.10.7-slim-bullseye

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

EXPOSE 80

WORKDIR /app

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80