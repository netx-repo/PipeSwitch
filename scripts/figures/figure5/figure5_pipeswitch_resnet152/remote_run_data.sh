# echo 'PipeSwitch demo: server creates Docker image for pipeswitch'
# echo

# Get current work dir
WORK_DIR=$(pwd)/PipeSwitch
# echo 'Current work dir:' $WORK_DIR
# echo

# Import global variables
source $WORK_DIR/scripts/config/env.sh
# echo 'Import global variables'
# echo

PYTHONPATH=$WORK_DIR python $WORK_DIR/scripts/figures/figure5/figure5_pipeswitch_resnet152/remote_run_data.py