# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

echo "Plot figure 5: ResNet152, PipeSwitch"
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/figures/figure5/figure5_pipeswitch_resnet152/host_run_data.py $WORK_DIR/scripts/config/servers.txt