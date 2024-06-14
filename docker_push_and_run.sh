#!/bin/bash

# Define variables
LLAMA_CPP_SERVER_IMAGE="ghcr.io/eericheva/llama_cpp_server_image:latest"
IMITATION_GAME_IMAGE="ghcr.io/eericheva/imitation_game_image:latest"

echo "Building LLAMA_CPP_SERVER_IMAGE..."
docker build -t $LLAMA_CPP_SERVER_IMAGE -f Dockerfile_llama_cpp_server ./llama_cpp_server
echo "Pushing LLAMA_CPP_SERVER_IMAGE..."
docker push $LLAMA_CPP_SERVER_IMAGE

echo "Building IMITATION_GAME_IMAGE..."
docker build -t $IMITATION_GAME_IMAGE -f Dockerfile_ig ./ig_app
echo "Pushing LLAMA_CPP_SERVER_IMAGE..."
docker push $IMITATION_GAME_IMAGE

# Pull the image and run the container
docker-compose up -d
