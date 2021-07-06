# ##############################
# ### Create the environment ###

# # Build basic Docker image on host
# bash scripts/environment/host_build_docker_image_base.sh

# # Export basic Docker image on host
# bash scripts/environment/host_export_docker_image_base.sh

# Copy basic Docker image to servers
# bash scripts/environment/host_push_docker_image_base.sh

# Load basic Docker image on servers
# bash scripts/environment/host_build_docker_image_pipeswitch.sh
# bash scripts/environment/host_build_docker_image_ready_model.sh
# bash scripts/environment/host_build_docker_image_mps.sh


# ### Create the environment END ###
# ##################################

# ####################
# ### Plot figures ###

# mkdir output

# PLot figure 5
# bash scripts/figures/plot_figure.sh figure5

# PLot figure 6
bash scripts/figures/plot_figure.sh figure6

# ### Plot figures END ###
# ########################