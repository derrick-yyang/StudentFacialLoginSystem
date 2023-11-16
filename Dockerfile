# Use a base OS image
FROM ubuntu:20.04

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY ./FaceRecognition /app/FaceRecognition
COPY ./pyqt_demo /app/pyqt_demo
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Set the entry point
# ENTRYPOINT [ "python3", "/app/pyqt_demo/main.py" ]