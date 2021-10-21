import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'pipeswitch',
    'per_layer',
    'grouped',
    'per_layer_no_pipeline'
]

models = [
    'resnet152',
    'inception_v3',
    'bert_base',
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
            print (output)
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
    # data = {}
    # for system in systems:
    #     data[system] = {}
    #     for model in models:
    #         data[system][model] = 100

    return data

def process_data(data):
    pipeswitch = [
        data['pipeswitch']['resnet152'], 
        data['pipeswitch']['inception_v3'], 
        data['pipeswitch']['bert_base']
    ]
    per_layer = [
        data['per_layer']['resnet152'], 
        data['per_layer']['inception_v3'], 
        data['per_layer']['bert_base']
    ]
    grouped = [
        data['grouped']['resnet152'], 
        data['grouped']['inception_v3'], 
        data['grouped']['bert_base']
    ]
    per_layer_no_pipeline = [
        data['per_layer_no_pipeline']['resnet152'], 
        data['per_layer_no_pipeline']['inception_v3'], 
        data['per_layer_no_pipeline']['bert_base']
    ]
    return pipeswitch, per_layer, grouped, per_layer_no_pipeline

def plot_figure(data):
    file_name = "output/figure7.pdf"
    sys_name = "PipeSwitch"

    models = ["ResNet152", "Inception_v3", "Bert_base"]
    our_sys, per_layer_pipe, one_batch_pipe, per_layer_nopipe = data

    x = np.arange(len(models))
    width = 0.4

    # setup font size
    font_size = 18
    plt.rc('font',**{'size': font_size, 'family': 'Arial' })
    plt.rc('pdf',fonttype = 42)

    fig, ax = plt.subplots(figsize=(8, 3.69))
    n = 4

    rects1 = ax.bar(x - 2 * width/n, our_sys, width/n, 
                    edgecolor='black', linewidth=0.5, label=sys_name)
    rects2 = ax.bar(x - width/n, per_layer_pipe, width/n,
                    edgecolor='black', linewidth=0.5,
                    label='Per-layer pipeline')
    rects3 = ax.bar(x , one_batch_pipe, width/n, 
                    edgecolor='black', linewidth=0.5,
                    label='Grouped transmission')
    rects4 = ax.bar(x + width/n, per_layer_nopipe, width/n,
                    edgecolor='black', linewidth=0.5, label="No optimization")
    ax.set_ylim((0,100))
    ax.set_ylabel('Latency (ms)')
    # ax.set_title('End to End Latency: vs Simple Transmission (V100)')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend(frameon=False, ncol=1, loc='upper center', 
            bbox_to_anchor=(0.3, 0.6, 0.5, 0.5),
            prop={'size': font_size-1})

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # fig.tight_layout()

    # plt.show()
    plt.savefig(file_name, format="pdf")

def main():
    # Collect data with experiments
    data = collect_data()
    print (data)

    # data = {'pipeswitch': {'resnet152': 41.25771522521973, 'inception_v3': 41.01982116699219, 'bert_base': 53.63037586212158}, 'per_layer': {'resnet152': 76.81310176849365, 'inception_v3': 53.38025093078613, 'bert_base': 69.2216157913208}, 'grouped': {'resnet152': 60.76028347015381, 'inception_v3': 45.93164920806885, 'bert_base': 83.79333019256592}, 'per_layer_no_pipeline': {'resnet152': 85.13836860656738, 'inception_v3': 60.726237297058105, 'bert_base': 93.85206699371338}}

    # Process data
    data = process_data(data)

    # Plot the figure
    plot_figure(data)
 

if __name__ == '__main__':
    main()