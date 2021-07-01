# echo 'PipeSwitch demo: host creates Docker images'
# echo

# Get current work dir
WORK_DIR=$(pwd)
mkdir $WORK_DIR/tmp
# echo 'Current work dir:' $WORK_DIR
# echo

# Import global variables
source $WORK_DIR/config/env.sh
# echo 'Import global variables'
# echo

# Copy the base docker to the server
echo 'Copy docker image for base to servers'
python scripts/environment/host_push_docker_image_base.py $WORK_DIR/scripts/config/servers.txt $WORK_DIR/tmp/$DOCKER_IMAGE_BASE_FILENAME
echo 'Complete loading docker image for base to servers'
echo