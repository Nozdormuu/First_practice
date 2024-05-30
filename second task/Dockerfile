FROM apache/airflow:2.0.1
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
FROM python:3.9
COPY . /app
RUN pip install -r /app/requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/path/to/credentials.json
CMD ["python", "/app/main.py"]