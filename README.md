# UOL Project

## Prerequisites

- Docker installed on your system.
- GNU Make installed on your system.

## Makefile Targets

The Makefile in this project provides the following targets:

- `build` - Build the Docker image.
- `run` - Run the Docker container.
- `stop` - Stop and remove the Docker container if it exists.
- `clean` - Remove the Docker image and container.

## Usage

### Build the Docker Image

To build the Docker image, run the following command:

```sh
make build
```

### Run the Docker Container

To run the Docker container, ensuring any existing container with the same name is stopped and removed first, run:

```sh
make run
```

### Stop and Remove the Docker Container

To stop and remove the Docker container if it exists, run:

```sh
make stop
```

### Clean Up Docker Image and Container

To clean up and remove both the Docker image and container, run:

```sh
make clean
```

## Example Workflow

Here's an example workflow to build and run the Docker container:

1. **Build the Docker image**:

   ```sh
   make build
   ```

2. **Run the Docker container**:

   ```sh
   make run
   ```

3. **Stop and remove the Docker container**:

   ```sh
   make stop
   ```

4. **Clean up the Docker image and container**:
   ```sh
   make clean
   ```
