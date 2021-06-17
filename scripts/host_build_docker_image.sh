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
echo

# Export the base docker image as a tar file
echo 'Export docker image:' $DOCKER_IMAGE_BASE_TAG
docker save -o $WORK_DIR/$DOCKER_IMAGE_BASE_FILENAME $DOCKER_IMAGE_BASE_TAG
echo 'Complete exporting docker image:' $DOCKER_IMAGE_BASE_FILENAME
echo

# Copy the base docker to the server
echo 'Copy docker image to servers'
python scripts/copy_image.py $WORK_DIR/config/servers.txt $WORK_DIR/$DOCKER_IMAGE_BASE_FILENAME
echo 'Complete copying docker image to servers'
echo

# Clone PipeSwitch repo to the server
echo 'Clone Pipewitch code to the server'
ssh aws-pipeswitch-opesource 'git clone --branch dev-dockerfile-base git@github.com:baizh1994/PipeSwitch.git'
echo

# Load the base docker on the server