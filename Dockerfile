FROM python:3.9-slim-buster

# Copy requirements file and install dependencies
COPY  . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN  cd src


ENV PYTHONUNBUFFERED=TRUE

ENTRYPOINT ["python3"]