echo 'PipeSwitch demo: create Docker images'
echo

# Get current work dir
WORK_DIR=$(pwd)
echo 'Current work dir:' $WORK_DIR
echo

# Import global variables
source $WORK_DIR/config/env.sh
echo 'Import global variables'
echo

# Build the image bash, which compiles PyTorch from source
echo 'Create docker image:' $DOCKER_IMAGE_BASE_TAG
docker build -t $DOCKER_IMAGE_BASE_TAG $WORK_DIR/Dockerfile
echo 'Complete creating docker image:' $DOCKER_IMAGE_BASE_TAG