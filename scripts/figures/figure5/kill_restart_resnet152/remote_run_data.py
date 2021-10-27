import os
import sys

from scripts.common.util import RunDocker

def main():
    with RunDocker('pipeswitch:ready_model', 'figure5_kill_restart_resnet152') as rd:
        # Start the server: ready_model
        print ('Server python start')
        rd.run('python PipeSwitch/scripts/run_data.py')
        print ('Server python end')
        
        # Get and return the data point

if __name__ == '__main__':
    main()