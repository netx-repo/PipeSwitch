##############################
### Create the environment ###

# Build basic Docker image on host
bash scripts/environment/host_build_docker_image_base.sh

# Export basic Docker image on host
bash scripts/environment/host_export_docker_image_base.sh

# Copy basic Docker image to servers
bash scripts/environment/host_push_docker_image_base.sh

# Load basic Docker image on servers
bash scripts/environment/ssh_load_docker_image_base.sh


### Create the environment END ###
##################################


# Plot each figure