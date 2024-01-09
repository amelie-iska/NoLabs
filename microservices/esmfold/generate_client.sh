#!/bin/bash

# Make sure Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker."
    exit
fi

# Make sure npx is installed
if ! command -v npx &> /dev/null
then
    echo "npx could not be found. Please install Node.js and npm."
    exit
fi

echo 'Installation: https://openapi-generator.tech/docs/installation'

DOCKER_IMAGE_NAME="esmfold_app_cuda11"

# Run the Docker container in the background
# Replace the Docker image name with the appropriate one
docker run -d --name esmfold --gpus all -e HOST=0.0.0.0 -e PORT=5731 -p 5731:5731 $DOCKER_IMAGE_NAME

# Generate the Python client using OpenAPI Generator
npx @openapitools/openapi-generator-cli generate \
    -i http://127.0.0.1:5731/openapi.json \
    -g python \
    -o ./client \
    --additional-properties=packageName=esmfold_microservice

echo 'Use pip install ./client'

# Note: The Docker container named 'esmfold' will continue to run. Stop and remove it if necessary.
