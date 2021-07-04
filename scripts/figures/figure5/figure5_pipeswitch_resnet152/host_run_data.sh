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

python scripts/figures/figure5/figure5_pipeswitch_resnet152/host_run_data.py $WORK_DIR/scripts/config/servers.txt