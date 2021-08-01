import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'pipeswitch', 
    'stop_next', 
    'kill_restart'
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
            print ('Plot figure 9: %s, %s' % (system, model))

            # Run the experiment
            result = subprocess.run(['bash', 'scripts/figures/figure9/%s_%s/host_run_data.sh' % (system, model)], stdout=subprocess.PIPE)

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
    # data = {}
    # for system in systems:
    #     data[system] = {}
    #     for model in models:
    #          data[system][model] = 100
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
    
    file_name = "output/figure9.pdf"
    sys_name = "PipeSwitch"

    models = ["ResNet152", "Inception_v3", "Bert_base"]
    our_sys, simple_switch, kill_restart = data

    x = np.arange(len(models))
    width = 0.5
    n = 3

    # setup font size
    font_size = 18
    plt.rc('font',**{'size': font_size, 'family': 'Arial' })
    plt.rc('pdf',fonttype = 42)

    # fig, ax = plt.subplots()
    fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, 
                                figsize=(8, 3.69),
                                gridspec_kw={'height_ratios': [1, 2]})
    plt.subplots_adjust(hspace=0.15)

    # upper part
    rects1 = ax.bar(x - width/n, our_sys, width/n, label=sys_name, 
                    edgecolor='black', linewidth=0.5,
                    )

    rects3 = ax.bar(x , simple_switch, width/n, label='One process', 
                    edgecolor='black', linewidth=0.5,)
    rects2 = ax.bar(x + width/n, kill_restart, width/n, label='Two processes', 
                    edgecolor='black', linewidth=0.5,)

    # bottom part
    rects2_1 = ax2.bar(x - width/n, our_sys, width/n, label=sys_name, 
                    edgecolor='black', linewidth=0.5,
                    )

    rects2_3 = ax2.bar(x , simple_switch, width/n, label='One process', 
                    linewidth=0.5,
                    edgecolor='black')
    rects2_2 = ax2.bar(x + width/n, kill_restart, width/n, label='Two processes', 
                    edgecolor='black', linewidth=0.5,)

    ax.set_ylim(6000, 9000)
    ax2.set_ylim(0, 250)

    # hide the spines between ax and ax2
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    ax.tick_params(bottom=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    # ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    # ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    ax.yaxis.set_label_coords(-0.12, -0.6)
    ax.set_ylabel('Latency (ms)')
    # ax.set_title('End to End Latency: vs Simple Transmission (V100)')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend(frameon=False, ncol=2, loc='upper left',
            bbox_to_anchor=(0.0, 1.1),
            prop={'size': font_size-1})

    # plt.show()
    plt.savefig(file_name, format="pdf")

def main():
    # Collect data with experiments
    data = collect_data()
    # Process data
    data = process_data(data)

    # Plot the figure
    plot_figure(data)
    


if __name__ == '__main__':
    main()