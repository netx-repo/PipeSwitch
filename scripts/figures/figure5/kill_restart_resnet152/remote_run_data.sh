# Get current work dir
WORK_DIR=$(pwd)/PipeSwitch

# Import global variables
source $WORK_DIR/scripts/config/env.sh

echo 'Server bash start'
PYTHONPATH=$PYTHONPATH:$WORK_DIR python $WORK_DIR/scripts/figures/figure5/kill_restart_resnet152/remote_run_data.py
echo 'Server bash end'