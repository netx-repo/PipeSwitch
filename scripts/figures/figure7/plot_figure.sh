# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

echo "Plot $FIGURE_INDEX"
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/figures/figure7/host_run_figure.py
echo "Complete ploting $FIGURE_INDEX"
echo