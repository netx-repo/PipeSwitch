# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

# Build the image bash, which compiles PyTorch from source
echo 'Create docker image:' $DOCKER_IMAGE_BASE_TAG
docker build -t $DOCKER_IMAGE_BASE_TAG -f $WORK_DIR/Dockerfile/Dockerfile-base $WORK_DIR/Dockerfile
echo 'Complete creating docker image:' $DOCKER_IMAGE_BASE_TAG
echo