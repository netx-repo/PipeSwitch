# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

LABEL=$1
IMAGE=$2
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/figures/host_run_data.py $WORK_DIR/scripts/config/servers.txt $LABEL $IMAGE