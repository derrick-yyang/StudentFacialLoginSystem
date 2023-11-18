# Base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Copy the pyqt_demo folder to the container
COPY pyqt_demo /app/pyqt_demo

# Copy the requirements.txt file to the container
COPY requirements.txt /app/requirements.txt

# Update package lists and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl

# Add deadsnakes PPA and install Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10

# Set the default Python version to 3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

# Install dependencies from requirements.txt
RUN python3 -m pip install -r requirements.txt

# # Set the entrypoint command
# CMD ["python3", "/app/pyqt_demo/main.py"]
