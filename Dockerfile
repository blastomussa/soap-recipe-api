FROM python:3.10.7-slim-bullseye

ENV DOCKER_IMG=true

WORKDIR /API

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 80

WORKDIR /API/app

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80

# Docker cmds to test image
#

# docker buildx build --platform linux/amd64 . #for amd64
# docker build -t apiimage .
# docker run -d --name apicontainer -p 80:80 apiimage
# docker tag myimage blastomussa/soap-recipe-api
# docker push blastomussa/soap-recipe-api