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
    # sys_name = "PipeSwitch"
    # file_name = "output/figure8.pdf"

    # models = [
    #     "ResNet152", 
    #     "Inception_v3", 
    #     # "Bert_base"
    # ]
    # # ready_model = [33.260075, 30.04206, 48.017385]
    # # pipeswitch = [39.275564, 35.448869, 58.291377]
    # # mps = [340.283585, 262.294412, 252.533078]
    # # kill_restart = [6508.667618, 7566.112161, 6419.338626]
    # ready_model, pipeswitch, mps, kill_restart = data

    # x = np.arange(len(models))
    # width = 0.8
    # n = 4

    # # setup font size
    # font_size = 18
    # plt.rc('font',**{'size': font_size, 'family': 'Arial' })
    # plt.rc('pdf',fonttype = 42)

    # # fig, ax = plt.subplots()
    # fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 3.69),
    #                             gridspec_kw={'height_ratios': [1, 2]})

    # plt.subplots_adjust(hspace=0.15)

    # # upper part
    # rects1 = ax.bar(x - 1 * width/n, ready_model, width/n, label='Ready model', 
    #                 edgecolor='black', linewidth=0.5, color="k"
    #                 )

    # rects4 = ax.bar(x , pipeswitch, width/n, label=sys_name,
    #                 linewidth=0.5,
    #                 edgecolor='black', color="tab:blue")

    # # rects5 = ax.bar(x , unified_memory, width/n, label="Unified Memory",
    # #                 linewidth=0.5,
    # #                 edgecolor='black')

    # rects3 = ax.bar(x + width/n, mps, width/n, label='MPS', 
    #                 edgecolor='black', linewidth=0.5, color="tab:green")

    # rects2 = ax.bar(x + 2 * width/n, kill_restart, width/n, label='Stop-and-start', 
    #                 edgecolor='black', linewidth=0.5, color="tab:orange")

    # # bottom part

    # rects2_1 = ax2.bar(x - width/n, ready_model, width/n, label='Ready model', 
    #                 edgecolor='black', linewidth=0.5, color='k'
    #                 )
    # rects2_4 = ax2.bar(x , pipeswitch, width/n, label=sys_name,
    #                 linewidth=0.5,
    #                 edgecolor='black', color="tab:blue")

    # # rects2_5 = ax2.bar(x, unified_memory, width/n, label="Unified Memory",
    # #                 linewidth=0.5,
    # #                 edgecolor='black')

    # rects2_3 = ax2.bar(x + width/n, mps, width/n, label='MPS', 
    #                 linewidth=0.5,
    #                 edgecolor='black', color="tab:green")

    # rects2_2 = ax2.bar(x + 2 * width/n, kill_restart, width/n, label='Stop-and-start', 
    #                 edgecolor='black', linewidth=0.5, color="tab:orange")

    # ax.set_ylim(6000, 10000)
    # ax2.set_ylim(0, 400)

    # # hide the spines between ax and ax2
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax2.spines['top'].set_visible(False)
    # ax2.spines['right'].set_visible(False)

    # ax.tick_params(bottom=False)  # don't put tick labels at the top
    # ax2.xaxis.tick_bottom()

    # d = .015  # how big to make the diagonal lines in axes coordinates
    # # arguments to pass to plot, just so we don't keep repeating them
    # kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    # ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    # # ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    # kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    # ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    # # ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # ax.yaxis.set_label_coords(-0.12, -0.6)
    # ax.set_ylabel('Latency (ms)')
    # # ax.set_title('End to End Latency: vs Simple Transmission (V100)')
    # ax.set_xticks(x)
    # ax.set_xticklabels(models)
    # ax.legend(
    #     frameon=False, ncol=2,
    #         loc='upper left', bbox_to_anchor=(0.0, 0.8, 0.5, 0.5),
    #         prop={'size': font_size-1})

    # # plt.show()
    # plt.savefig(file_name, format="pdf")
    return None

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