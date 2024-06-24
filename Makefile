# Variables
IMAGE_NAME = uol
CONTAINER_NAME = uol_container
PORT = 80

# Default target
.PHONY: all
all: build run

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
.PHONY: run
run: stop
	docker run --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Stop and remove the Docker container if it exists
.PHONY: stop
stop:
	@if [ `docker ps -a -q -f name=$(CONTAINER_NAME)` ]; then \
		docker stop $(CONTAINER_NAME); \
		docker rm $(CONTAINER_NAME); \
	fi

# Clean up the Docker image and container
.PHONY: clean
clean: stop
	@if [ `docker images -q $(IMAGE_NAME)` ]; then \
		docker rmi $(IMAGE_NAME); \
	fi