FROM python:3.10.7-slim-bullseye

# Install git
RUN apt-get -y update
RUN apt-get -y install git

# Clone github repository
RUN git clone https://github.com/blastomussa/soap-recipe-api /API
WORKDIR /API

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

EXPOSE 80

WORKDIR /API/app

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80