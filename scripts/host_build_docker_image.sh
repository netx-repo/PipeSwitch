echo 'PipeSwitch demo: host creates Docker images'
echo

# Get current work dir
WORK_DIR=$(pwd)
mkdir $WORK_DIR/tmp
echo 'Current work dir:' $WORK_DIR
echo

# Import global variables
source $WORK_DIR/config/env.sh
echo 'Import global variables'
echo

# Build the image bash, which compiles PyTorch from source
echo 'Create docker image:' $DOCKER_IMAGE_BASE_TAG
docker build -t $DOCKER_IMAGE_BASE_TAG $WORK_DIR/Dockerfile-base
echo 'Complete creating docker image:' $DOCKER_IMAGE_BASE_TAG
echo

# Export the base docker image as a tar file
echo 'Export docker image:' $DOCKER_IMAGE_BASE_TAG
docker save -o $WORK_DIR/tmp/$DOCKER_IMAGE_BASE_FILENAME $DOCKER_IMAGE_BASE_TAG
echo 'Complete exporting docker image:' $DOCKER_IMAGE_BASE_FILENAME
echo

# Copy the base docker to the server
echo 'Copy docker image for base to servers'
python scripts/host_push_docker_image_base.py $WORK_DIR/config/servers.txt $WORK_DIR/tmp/$DOCKER_IMAGE_BASE_FILENAME
echo 'Complete loading docker image for base to servers'
echo

# Build the pipeswitch docker on the server
echo 'Build docker image for pipeswitch on servers'
python scripts/host_remote_build_docker_image_pipeswitch.py $WORK_DIR/config/servers.txt
echo 'Complete building docker image for pipeswitch to servers'
echo