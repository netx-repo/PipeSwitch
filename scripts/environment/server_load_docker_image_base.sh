# Get current work dir
WORK_DIR=$(pwd)/PipeSwitch

# Import global variables
source $WORK_DIR/scripts/config/env.sh

# Import docker image
echo 'Import docker image:' $DOCKER_IMAGE_BASE_TAG
docker load -i ~/$DOCKER_IMAGE_BASE_FILENAME
echo 'Complete importing docker image:' $DOCKER_IMAGE_BASE_FILENAME
echo