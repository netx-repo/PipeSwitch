import os
import sys

from scripts.common.util import RunDocker

def main():
    with RunDocker('pytorch/pytorch:1.3-cuda10.1-cudnn7-devel', 'dev') as rd:
        # Start the server: ready_model
        rd.run('python PipeSwitch/scripts/environment/container_run_warmup.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()