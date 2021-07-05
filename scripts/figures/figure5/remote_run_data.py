import os
import sys

from scripts.common.util import RunDocker

def main():
    label = sys.argv[1]
    with RunDocker('pipeswitch:ready_model', 'ready_model', label) as rd:
        # Start the server: ready_model
        rd.run('python PipeSwitch/scripts/run_data.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()