import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'pipeswitch', 
    'no_memory_management', 
    'no_ipc_optimization',
    'no_pin',
    'unified_memory'
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
            print ('Plot figure 8: %s, %s' % (system, model))

            # Run the experiment
            result = subprocess.run(['bash', 'scripts/figures/figure8/%s_%s/host_run_data.sh' % (system, model)], stdout=subprocess.PIPE)

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
    pipeswitch = [
        data['pipeswitch']['resnet152'], 
        data['pipeswitch']['inception_v3'], 
        data['pipeswitch']['bert_base']
    ]
    stop_next = [
        data['stop_next']['resnet152'], 
        data['stop_next']['inception_v3'], 
        data['stop_next']['bert_base']
    ]
    kill_restart = [
        data['kill_restart']['resnet152'], 
        data['kill_restart']['inception_v3'], 
        data['kill_restart']['bert_base']
    ]
    return pipeswitch, stop_next, kill_restart

def plot_figure(data):
    %matplotlib inline
    import matplotlib.pyplot as plt
    import palettable

    # Component - Memory
    # Latency v.s. Method
    file_label = 'component_memory_v100'

    # data
    y_sys = [39.275564, 35.448869, 58.291377]
    y_malloc = [62.69336, 46.950152, 76.815955]
    y_ipc = [87.570691, 58.538342, 94.64469]
    y_no_pin = [53.502496, 43.420611, 62.364679]
    y_um = [184.045815, 223.192644, 229.593801]


    # labels for x
    x_label = 'Models'
    width = 0.15
    index_sys = [i + 0.7 for i in range(3)]
    index_malloc = [i + 0.85 for i in range(3)]
    index_ipc = [i + 1.0 for i in range(3)]
    index_no_pin = [i + 1.15 for i in range(3)]
    index_um = [i + 1.3 for i in range(3)]

    x_ticks = [i + 1.0 for i in range(3)]
    x_ticklabels = ["ResNet152", "Inception_v3", "Bert_base"]

    # labels for y
    y_label = 'Latency (ms)'
    y_ticks = [i * 100 for i in range(5)]
    y_ticklabels = [str(i * 100) for i in range(5)]

    font_size = 23
    plt.rc('font',**{'size': font_size, 'family': 'Arial' })
    plt.rc('pdf',fonttype = 42)
    fig, ax = plt.subplots(figsize=(13, 6))

    # Plot bars
    b1 = plt.bar(index_sys, y_sys, width, zorder=3, clip_on=False, edgecolor='black')
    b2 = plt.bar(index_malloc, y_malloc, width, zorder=3, clip_on=False, edgecolor='black')
    b3 = plt.bar(index_ipc, y_ipc, width, zorder=3, clip_on=False, edgecolor='black')
    b4 = plt.bar(index_no_pin, y_no_pin, width, zorder=3, clip_on=False, edgecolor='black')
    b5 = plt.bar(index_um, y_um, width, zorder=3, clip_on=False, edgecolor='black')
    plt.legend((b1, b2, b3, b4, b5), 
            (sysname, 'No memory management', 'No IPC optimization', 'No pin memory', 'CUDA unified memory'), 
            loc='upper left',ncol=2, frameon=False, prop={'size':font_size})

    ax.tick_params(labelsize=font_size, pad=10)

    # Plot x labels
    # ax.set_xlabel(x_label)
    # ax.set_xlim(left=0, right=4)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticklabels)

    # Plot y labels
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom=0, top=400)
    ax.yaxis.set_ticks_position('left')
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticklabels)


    ax.get_yaxis().set_tick_params(direction='in')
    ax.get_xaxis().set_tick_params(direction='in')

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')


    plt.savefig('Eval_%s.pdf' % (file_label), bbox_inches='tight', transparent = True)

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