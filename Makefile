IMAGE_NAME = facerecognition
CONTAINER_NAME = FaceRecognition

.PHONY: build run start connect stop remove purge

build:
	sudo docker build -t $(IMAGE_NAME) .

run:
	docker run -it -v "$(PWD)/FaceRecognition:/app/FaceRecognition" -v "$(PWD)/pyqt_demo:/app/pyqt_demo" --name $(CONTAINER_NAME) $(IMAGE_NAME)

start:
	docker start $(IMAGE_NAME)

connect:
	docker exec -it $(CONTAINER_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)

remove:
	docker rm $(CONTAINER_NAME)

purge:
	docker rm $(CONTAINER_NAME)
	docker rmi $(IMAGE_NAME)