#!/bin/bash

# Get the current timestamp
current_time=$(date +%s)

# List all running containers
docker ps -q --filter status=running | while read -r container_id; do
    # Get the creation time of the container
    creation_time=$(docker inspect -f '{{.Created}}' "$container_id")
    
    # Get the name of the container
    container_name=$(docker inspect -f '{{.Name}}' "$container_id" | sed 's/^\/\(.*\)$/\1/')

    # Convert the creation time to a timestamp
    creation_timestamp=$(date --date="$creation_time" +%s)
    
    # Calculate the age of the container in seconds
    age=$((current_time - creation_timestamp))

    # If the container is older than 1 second, remove it
    if [ $age -gt 1200 ]; then
        docker rm -f "$container_id"
        echo "Deleted container $container_id created at $creation_time"

        json_payload=$(jq -n \
          --arg container_name "$container_name" \
          '{container_name: $container_name}')

        # Send HTTP POST request
        curl -X POST "https://cyber.hypershacker.space/disconnect/" \
          -H "Content-Type: application/json" \
          -d "$json_payload"
    fi
done

# Prune unused networks
docker network prune -f
echo "Pruned unused networks"