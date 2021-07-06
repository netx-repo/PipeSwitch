import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'ready_model',
    # 'pipeswitch', 
    # 'mps', 
    # 'kill_restart'
]

intervals = [
    '1s',
    '2s',
    '5s',
    '10s',
    # '30s'
]

def collect_data():
    data = {}
    for system in systems:
        data[system] = {}
        for interval in intervals:
            print ('Plot figure 6: %s, %s' % (system, interval))

            # Run the experiment
            result = subprocess.run(['bash', 'scripts/figures/host_run_data.sh',  'figure6_%s_%s' % (system, interval)], stdout=subprocess.PIPE)

            # Get output
            output = result.stdout.decode('utf-8')
            lines = output.split('\n')
            for line in lines:
                line = line.strip()
                if OUTPUT_FLAG in line:
                    parts = line.split(',')
                    throughput  = float(parts[1].strip())
                    latency_avg = float(parts[2].strip())
                    latency_min = float(parts[3].strip())
                    latency_max = float(parts[4].strip())
                    data[system][interval] = [throughput, latency_avg, latency_min, latency_max]
                    break
    
    return data

def process_data(data):
    return None

def plot_figure(data):
    pass

def main():
    # Collect data with experiments
    data = collect_data()
    print (data)
    return

    # Process data
    data = process_data(data)

    # Plot the figure
    plot_figure(data)
    


if __name__ == '__main__':
    main()