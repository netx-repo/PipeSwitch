# Get current work dir
WORK_DIR=$(pwd)
mkdir $WORK_DIR/tmp

# Import global variables
source $WORK_DIR/scripts/config/env.sh

# Export the base docker image as a tar file
echo 'Export docker image:' $DOCKER_IMAGE_BASE_TAG
docker save -o $WORK_DIR/tmp/$DOCKER_IMAGE_BASE_FILENAME $DOCKER_IMAGE_BASE_TAG
echo 'Complete exporting docker image:' $DOCKER_IMAGE_BASE_FILENAME
echo