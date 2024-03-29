#!/bin/bash

container_name='anemometer-test'

# Function to wait for container to be healthy
wait_for_container_health() {
    timeout=60
    while [[ $timeout -gt 0 ]]; do
        # Check if container has a health check defined
        if docker inspect --format='{{.State.Health}}' $1 > /dev/null 2>&1; then
            if docker inspect --format='{{.State.Health.Status}}' $1 | grep -q "healthy"; then
                echo "Container is healthy."
                return 0
            fi
        else
            # If health check is not defined, consider container as healthy if it's running
            if [ "$(docker inspect --format '{{.State.Status}}' $1)" == "running" ]; then
                echo "Container is running but does not have a health check defined."
                return 0
            fi
        fi
        sleep 1
        ((timeout--))
    done
    echo "Timed out waiting for the container to be healthy."
    return 1
}


# Check if the container already exists
if docker ps -a --format '{{.Names}}' | grep -q $container_name; then
    echo "Container '$container_name' already exists."
    CONTAINER_ID=$(docker ps --format '{{.ID}}' --filter "name=$container_name")

    if [ "$(docker inspect --format '{{.State.Status}}' $CONTAINER_ID)" == "running" ]; then
        echo "Container is running, using the existing container..."
    else
        echo "Container is not running, starting it..."
        docker start $container_name
        # Introduce a delay until the container is healthy
        if ! wait_for_container_health $CONTAINER_ID; then
            echo "Error: Container initialization failed. Exiting."
            exit 1
        fi
    fi
else
    echo "Container '$container_name' does not exist, creating it..."
    CONTAINER_ID=$(docker run --rm -d --name $container_name --privileged --entrypoint /bin/bash arm32v7/ubuntu:latest)
    echo "Container ID after creation: $CONTAINER_ID"

    # Introduce a delay for container initialization
    if ! wait_for_container_health $CONTAINER_ID; then
        echo "Error: Container initialization failed. Exiting."
        exit 1
    fi
fi

if [ -z "$CONTAINER_ID" ]; then
    echo "Failed to create or retrieve container ID. Exiting."
    exit 1
fi

# Check if the container exists before proceeding
if docker ps -a --format '{{.ID}}' | grep -q $CONTAINER_ID; then
    echo "Container exists, proceeding with package installation..."
else
    echo "Error: Container does not exist. Exiting."
    exit 1
fi


# Check if container creation was successful
if [ -z "$CONTAINER_ID" ]; then
    echo "Failed to create or retrieve container ID. Exiting."
    exit 1
fi

# Print container ID
echo "Container ID: $CONTAINER_ID"

# Check if the container exists before executing commands
if docker ps -a --format '{{.ID}}' | grep -q $CONTAINER_ID; then
    echo "Container exists, proceeding with package installation..."

    # Install necessary packages if they are not installed
    echo "Installing necessary packages..."
    docker exec $CONTAINER_ID bash -c 'which node npm python3 pip3 tsc curl wget' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Installing necessary packages..."
        docker exec $CONTAINER_ID bash -c 'which python3' > /dev/null 2>&1 || docker exec $CONTAINER_ID apt-get install -y python3
        docker exec $CONTAINER_ID bash -c 'which pip3' > /dev/null 2>&1 || docker exec $CONTAINER_ID apt-get install -y python3-pip
        docker exec $CONTAINER_ID bash -c 'which curl' > /dev/null 2>&1 || docker exec $CONTAINER_ID apt-get install -y curl
        docker exec $CONTAINER_ID bash -c 'which wget' > /dev/null 2>&1 || docker exec $CONTAINER_ID apt-get install -y wget
        docker exec $CONTAINER_ID apt-get install -y --upgrade setuptools
        docker exec $CONTAINER_ID bash -c 'which RPI.GPIO' > /dev/null 2>&1 || docker exec $CONTAINER_ID apt-get install -y RPI.GPIO
        docker exec $CONTAINER_ID bash -c 'which adafruit-blinka' > /dev/null 2>&1 || docker exec $CONTAINER_ID apt-get install -y adafruit-blinka
    else
        echo "Necessary packages are already installed."
    fi

    # Update and upgrade packages
    docker exec $CONTAINER_ID apt-get update -y
    docker exec $CONTAINER_ID apt-get upgrade -y

    # Set display for GUI applications if needed
    docker exec $CONTAINER_ID /bin/bash -c "export DISPLAY=\$(cat /etc/resolv.conf | grep nameserver | awk '{print \$2}'):0"

    # Clone Anemometer repository if not already cloned
    if docker exec $CONTAINER_ID ls anemometer &> /dev/null; then
        echo "Anemometer is already cloned in the container."
    else
        echo "Cloning Anemometer repository..."
        docker exec $CONTAINER_ID git clone https://github.com/jonathan-99/anemometer.git anemometer
    fi

    # Print OS version
    echo "OS Version:"
    docker exec $CONTAINER_ID cat /etc/os-release

    # Print Python version
    echo "Python Version:"
    docker exec $CONTAINER_ID python3 --version

    # Print unittest version
    echo "unittest Version:"
    docker exec $CONTAINER_ID python3 -m unittest

    # Print coverage version
    echo "coverage Version:"
    docker exec $CONTAINER_ID coverage --version

    # Print Docker image ID
    echo "Docker Image ID:"
    docker exec $CONTAINER_ID cat /proc/self/cgroup | grep "docker" | sed 's/^.*\///' | head -n 1

else
    echo "Error: Container does not exist. Exiting."
    exit 1
fi
