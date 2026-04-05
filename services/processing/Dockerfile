FROM python:3.11

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "worker.celery", "worker", "--loglevel=info"]