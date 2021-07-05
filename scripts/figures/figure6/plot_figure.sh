# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

echo "Plot figure 6"
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/figures/figure6/host_run_figure.py
echo "Complete ploting figure 6"
echo