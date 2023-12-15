# Use the official Ubuntu image as a parent image
FROM ubuntu:20.04

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.9 and pip
RUN apt-get update && apt-get install -y \
python3.10 \
python3-pip


# Upgrade pip and install the required Python packages.
RUN pip3 install --upgrade pip 
RUN pip3 install --default-timeout=1000 --ignore-installed flask
RUN pip3 install --default-timeout=1000 --ignore-installed pyyaml
RUN pip3 install --default-timeout=1000 --ignore-installed python-dateutil
RUN pip3 install --default-timeout=1000 --ignore-installed Flask-HTTPAuth