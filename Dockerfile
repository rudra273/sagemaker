FROM python:3.9-slim-buster

# Copy requirements file and install dependencies
COPY  ./src/ ./src/
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


ENV PYTHONUNBUFFERED=TRUE

ENTRYPOINT ["python3"]