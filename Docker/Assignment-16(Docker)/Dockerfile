FROM python:3.12-slim

RUN apt-get update && apt-get install -y openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pyspark==3.5.1

WORKDIR /app
COPY . .

CMD ["spark-submit", "spark_app.py"]