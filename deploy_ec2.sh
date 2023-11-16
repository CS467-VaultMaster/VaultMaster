#!/bin/bash

# Used to load new production images into Docker, on the EC2 server
# Run within EC2 after running "deploy_local.sh" locally

# Script halts if any command fails
set -e

# Load new images into Docker 
docker load -i vaultmaster_build.tar

# Delete .tar file
rm -vf vaultmaster_build.tar

# Delete older images
docker image prune -f

# Print success and reminder on how to start up
echo "Images loaded! Run 'docker compose -f docker-compose.prod.yml up' to start the server."