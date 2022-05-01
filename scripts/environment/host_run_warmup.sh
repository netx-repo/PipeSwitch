# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

# Copy the base docker to the server
echo 'Warm up servers'
PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/environment/host_run_warmup.py $WORK_DIR/scripts/config/servers.txt
echo 'Complete warming up servers'
echo