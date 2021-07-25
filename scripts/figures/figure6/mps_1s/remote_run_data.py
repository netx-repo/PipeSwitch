import os
import sys

from scripts.common.util import RunDocker

def main():
    with RunDocker('pipeswitch:mps', 'figure6_mps_1s') as rd:
        # Start the server: mps
        rd.run('python PipeSwitch/scripts/run_data.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()