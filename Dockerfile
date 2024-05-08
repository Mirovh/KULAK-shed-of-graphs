# Use an official Python runtime as a parent image
FROM ubuntu:22.04 as base

ENV DOCKER_CONTAINER 1

# Install python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container to /app
WORKDIR /app

# Add the app directory contents into the container at /app
ADD src/app /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Multi-stage build: create a test image
FROM base as test

# Install pytest
RUN pip install pytest

# Copy the test directory into the container at /test
COPY src/test /test

# Set the working directory in the container to /test
WORKDIR /test

# Run the tests
CMD ["pytest"]

# Multi-stage build: create a production image
FROM base as prod

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Install plantri
COPY src/plantri54 /plantri54
WORKDIR /plantri54
RUN make
# Add plantri to PATH
ENV PATH="/plantri54:${PATH}"
WORKDIR /app

# Define history location
ENV SOG_HISTORY_PATH /backup/hist

# Define img location
ENV SOG_IMG_PATH /backup/hist/img

RUN apt-get update && apt-get install -y tree

# Run hostServer.py when the container launches
CMD ["python3", "hostServer.py"]