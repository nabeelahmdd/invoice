# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container
COPY . /usr/src/app/
