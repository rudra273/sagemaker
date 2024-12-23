# FROM python:3.9-slim-buster

# # Copy all project files, including the src directory
# COPY . .

# # Install dependencies
# RUN pip3 install --no-cache-dir -r requirements.txt

# WORKDIR /src

# # Set the PYTHONPATH to include the src directory
# ENV PYTHONPATH=/src

# # Ensure Python output is not buffered
# ENV PYTHONUNBUFFERED=TRUE

# # Set the entrypoint for the container
# ENTRYPOINT ["python3"]


FROM python:3.9-slim-buster

# Create and set the working directory
WORKDIR /opt/ml/code

# Copy all project files to the working directory
COPY . .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH to include the source directory
ENV PYTHONPATH=/opt/ml/code

# Ensure Python output is not buffered
ENV PYTHONUNBUFFERED=TRUE

# Set the entrypoint
ENTRYPOINT ["python3"]