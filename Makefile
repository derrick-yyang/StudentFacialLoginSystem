IMAGE_NAME = facerecognition
CONTAINER_NAME = FaceRecognition

.PHONY: build run connect start stop remove purge

build:
	sudo docker build -t $(IMAGE_NAME) .

run:
	docker run -it -v "$(PWD)/pyqt_demo:/app/pyqt_demo" --name $(CONTAINER_NAME) $(IMAGE_NAME)

connect:
	docker exec -it $(CONTAINER_NAME) /bin/bash

start:
	docker start $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)

remove:
	docker rm $(CONTAINER_NAME)

purge:
	docker rm $(CONTAINER_NAME)
	docker rmi $(IMAGE_NAME)