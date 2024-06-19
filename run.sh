#!/bin/bash

# Command to build and start Docker containers
echo "Building and starting Docker containers..."
docker-compose up --build -d || { echo "Failed to build and start Docker containers"; exit 1; }
echo "Docker containers started successfully"

# Display running containers
echo "Running containers:"
docker ps

# Get container name based on image name
container_name="sms-campaigner-fast-api_web_1"

# Check if container name is found
if [ -z "$(docker ps --filter "name=$container_name" -q)" ]; then
  echo "Container $container_name not found. Exiting..."
  exit 1
fi

# Enter the Docker container shell
echo "Entering Docker container $container_name..."
docker exec -it $container_name /bin/bash || { echo "Failed to enter Docker container $container_name"; exit 1; }

# Apply migrations using Alembic inside the container
echo "Applying database migrations inside the container..."
docker exec -it $container_name alembic revision --autogenerate -m "Initial migration" || { echo "Failed to generate migration"; exit 1; }
docker exec -it $container_name alembic upgrade head || { echo "Failed to upgrade database"; exit 1; }
echo "Database migrations applied successfully"

# Exit from the Docker container shell
echo "Exiting Docker container $container_name..."
docker exec -it $container_name exit

# Displaying logs
echo "Displaying logs for all containers..."
docker-compose logs -f
