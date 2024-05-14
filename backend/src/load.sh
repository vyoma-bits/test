#!/bin/bash

# Read the .env file and export its contents
while IFS='=' read -r key value; do
  export "$key"="$value"
done < .env

# Optional: Print a message to confirm that the variables are exported
echo "Environment variables exported successfully."
