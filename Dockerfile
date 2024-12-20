FROM python:3.9-slim-buster

# Copy all project files, including the src directory
COPY . /app

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Ensure Python output is not buffered
ENV PYTHONUNBUFFERED=TRUE

# Set the entrypoint for the container
ENTRYPOINT ["python3"]
