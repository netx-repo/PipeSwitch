# ##############################
# ### Create the environment ###

# # Build basic Docker image on host
# bash scripts/environment/host_build_docker_image_base.sh

# # Export basic Docker image on host
# bash scripts/environment/host_export_docker_image_base.sh

# Copy basic Docker image to servers
# bash scripts/environment/host_push_docker_image_base.sh

# Load basic Docker image on servers
# bash scripts/environment/host_build_docker_image_ready_model.sh
# bash scripts/environment/host_build_docker_image_pipeswitch.sh
# bash scripts/environment/host_build_docker_image_mps.sh


# ### Create the environment END ###
# ##################################

# ####################
# ### Plot figures ###

# mkdir output

# Warm up servers
bash scripts/environment/host_run_warmup.sh

# PLot figure 5
bash scripts/figures/figure5/plot_figure.sh

# PLot figure 6
bash scripts/figures/figure6/plot_figure.sh

# PLot figure 7
bash scripts/figures/figure7/plot_figure.sh

# PLot figure 8
bash scripts/figures/figure8/plot_figure.sh

# PLot figure 9
bash scripts/figures/figure9/plot_figure.sh

# ### Plot figures END ###
# ########################