# echo 'PipeSwitch demo: host creates Docker images'
# echo

# Get current work dir
WORK_DIR=$(pwd)
mkdir $WORK_DIR/tmp
# echo 'Current work dir:' $WORK_DIR
# echo

# Import global variables
source $WORK_DIR/scripts/config/env.sh
# echo 'Import global variables'
# echo

# Build the pipeswitch docker on the server
echo 'Build docker image for pipeswitch on servers'
python scripts/host_build_docker_image_pipeswitch.py $WORK_DIR/scripts/config/servers.txt
echo 'Complete building docker image for pipeswitch to servers'
echo