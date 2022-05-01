# Get current work dir
WORK_DIR=$(pwd)/PipeSwitch

# Import global variables
source $WORK_DIR/scripts/config/env.sh

# Build the image bash, which compiles PyTorch from source
echo 'Create docker image:' $DOCKER_IMAGE_MPS_TAG
docker build -t $DOCKER_IMAGE_MPS_TAG -f $WORK_DIR/Dockerfile/Dockerfile-mps $WORK_DIR/Dockerfile
echo 'Complete creating docker image:' $DOCKER_IMAGE_MPS_TAG
echo