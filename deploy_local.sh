#!/bin/bash

# Used to build production images and push them to the server
# (Build process is now too resource-intensive to perform on server)

# Script halts if any command fails
set -e

# Load environment variables from .env.dev
set -a 
source .env.dev
set +a

# Build images
docker compose -f docker-compose.prod_build.yml build prod-server
#docker compose -f docker-compose.prod_build.yml build backend # TODO: this isn't playing nice for some reason

# Delete now-obsolete local images 
docker image prune -f

# Save images as .tar
docker save -o vaultmaster_build.tar vaultmaster-prod-server:latest #vaultmaster-backend:latest

# scp em over 
scp vaultmaster_build.tar "$SCP_TARGET"

# Delete local .tar files 
rm -vf vaultmaster_build.tar

echo "Images pushed! They can now be loaded into production within EC2."