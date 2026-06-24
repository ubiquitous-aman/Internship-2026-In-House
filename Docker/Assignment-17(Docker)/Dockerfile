FROM python:3.12-slim

RUN apt-get update && apt-get install -y openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pyspark==3.5.3

WORKDIR /app
COPY . .

CMD ["python3", "spark_app1.py"]