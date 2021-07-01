##############################
### Create the environment ###

# Build basic Docker image on host
bash scripts/environment/host_build_docker_image_base.sh

# Export basic Docker image on host

# Copy basic Docker image to servers
bash scripts/environment/host_push_docker_image_base.sh

# Load basic Docker image on servers


### Create the environment END ###
##################################


# Plot each figure