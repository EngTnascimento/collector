FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY . .

ARG RABBITMQ_PASSWORD

ENV RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD}

RUN apk update && apk add --no-cache git && \
  pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "run.py"]
