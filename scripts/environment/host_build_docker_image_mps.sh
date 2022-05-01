# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

# Build the MPS docker on the server
echo 'Build docker image for MPS on servers'
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/environment/host_build_docker_image_mps.py $WORK_DIR/scripts/config/servers.txt
echo 'Complete building docker image for MPS to servers'
echo