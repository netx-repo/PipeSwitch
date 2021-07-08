import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'pipeswitch',
    # 'per_layer',
    # 'grouped',
    # 'per_layer_no_pipeline'
]

models = [
    'resnet152',
    # 'inception_v3',
    # 'bert_base',
]

def collect_data():
    data = {}
    for system in systems:
        data[system] = {}
        for model in models:
            print ('Plot figure 7: %s, %s' % (system, model))

            # Run the experiment
            result = subprocess.run(['bash', 'scripts/figures/figure7/%s_%s/host_run_data.sh' % (system, model)], stdout=subprocess.PIPE)

            # Get output
            output = result.stdout.decode('utf-8')
            lines = output.split('\n')
            for line in lines:
                line = line.strip()
                if OUTPUT_FLAG in line:
                    parts = line.split(',')
                    latency = float(parts[1].strip())
                    stdev = float(parts[2].strip())
                    count = int(parts[3])
                    data[system][model] = latency
                    break
    
    return data

def process_data(data):
    return None

def plot_figure(data):
    pass

def main():
    # Collect data with experiments
    data = collect_data()
    # print (data)
    # return

    # Process data
    data = process_data(data)

    # Plot the figure
    plot_figure(data)
    
 

if __name__ == '__main__':
    main()