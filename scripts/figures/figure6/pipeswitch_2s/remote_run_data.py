import os
import sys

from scripts.common.util import RunDocker

def main():
    with RunDocker('pipeswitch:pipeswitch', 'figure6_pipeswitch_2s') as rd:
        # Start the server: pipeswitch
        rd.run('python PipeSwitch/scripts/run_data.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()