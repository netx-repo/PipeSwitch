# Get current work dir
WORK_DIR=$(pwd)/PipeSwitch

# Import global variables
source $WORK_DIR/scripts/config/env.sh

LABEL=$1
PYTHONPATH=$PYTHONPATH:$WORK_DIR python $WORK_DIR/scripts/figures/remote_run_data.py $LABEL