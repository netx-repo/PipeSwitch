# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

FIGURE_INDEX=$1
echo "Plot $FIGURE_INDEX"
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/figures/host_run_$FIGURE_INDEX.py
echo "Complete ploting $FIGURE_INDEX"
echo