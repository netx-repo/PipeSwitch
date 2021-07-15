# Get current work dir
WORK_DIR=$(pwd)/mps

# Import global variables
source $WORK_DIR/scripts/config/env.sh

PYTHONPATH=$PYTHONPATH:$WORK_DIR python $WORK_DIR/scripts/figures/figure6/mps_10s/remote_run_data.py