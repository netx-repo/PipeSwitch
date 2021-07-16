import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'ready_model',
    'pipeswitch', 
    'mps', 
    'kill_restart'
]

intervals = [
    '1s',
    '2s',
    '5s',
    '10s',
    '30s'
]

def collect_data():
    data = {}
    # for system in systems:
    #     data[system] = {}
    #     for interval in intervals:
    #         print ('Plot figure 6: %s, %s' % (system, interval))

    #         # Run the experiment
    #         result = subprocess.run(['bash', 'scripts/figures/figure6/%s_%s/host_run_data.sh' % (system, interval)], stdout=subprocess.PIPE)

    #         # Get output
    #         output = result.stdout.decode('utf-8')
    #         lines = output.split('\n')
    #         for line in lines:
    #             line = line.strip()
    #             if OUTPUT_FLAG in line:
    #                 parts = line.split(',')
    #                 throughput  = float(parts[1].strip())
    #                 latency_avg = float(parts[2].strip())
    #                 latency_min = float(parts[3].strip())
    #                 latency_max = float(parts[4].strip())
    #                 data[system][interval] = [throughput, latency_avg, latency_min, latency_max]
    #                 break
    for system in systems:
        data[system] = {}
        for interval in intervals:
            data[system][interval] = [30, 100, 90, 110]
    
    return data

def process_data_throughput(data):
    ret = []
    for system in systems:
        ret.append([])
        for interval in intervals:
            ret[-1].append(data[system][interval][0])
    return ret

def plot_figure_throughput(data):
    file_name = "output/figure6_throughput.pdf"

    ready_model, pipeswitch, mps, kill_restart = data
    upper_bound = ready_model[3] # ready_model_10s

    x = np.arange(len(intervals))
    width = 0.8
    n = 4

    font_size = 18
    plt.rc('font',**{'size': font_size, 'family': 'Arial' })
    plt.rc('pdf',fonttype = 42)

    fig, ax = plt.subplots(figsize=(8, 3.69))

    rects2 = ax.bar(x - width/n, kill_restart, width/n, label='Stop-and-start', linewidth=0.5,
                    edgecolor='black', color='tab:orange')

    rects3 = ax.bar(x , mps, width/n, label='MPS', linewidth=0.5,
                    edgecolor='black', color='tab:green')

    rects1 = ax.bar(x + width/n, pipeswitch, width/n, label='PipeSwitch', linewidth=0.5,
                    edgecolor='black', color='tab:blue')

    ax.set_ylabel('Throughput (batches/sec)')
    # ax.set_title('End to End Latency: vs Simple Transmission (V100)')
    ax.set_xticks(x)
    ax.set_xticklabels(intervals)
    ax.legend([rects1, rects3, rects2], ['PipeSwitch', 'MPS', 'Stop-and-start'],
    # ax.legend([rects1, rects2], ['PipeSwitch', 'Stop-and-start'],
        frameon=False, ncol=2, loc='upper left',
            bbox_to_anchor=(0.0, 1.05),
            prop={'size': font_size-1})

    # ax.set_ylim(0, 400)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axhline(upper_bound, ls='--', c='k')
    # ax.annotate('Upper bound', xy=(3.5, 260),  
    #             xytext=(3.5, 300),
    #             arrowprops=dict(facecolor='black', arrowstyle='-|>'),
    #             fontsize=13
    #             )

    # fig.tight_layout()

    # plt.show()
    plt.savefig(file_name, format="pdf")

def process_data_latency(data):
    ret = []
    for system in systems:
        ret.append([])
        ret.append([])
        for interval in intervals:
            ret[-2].append(data[system][interval][1])
            ret[-1].append((data[system][interval][2], data[system][interval][3]))
    return ret

def plot_figure_latency(data):
    file_name = "output/figure6_latency.pdf"

    ready_model, ready_model_yerr, pipeswitch, pipeswitch_yerr, mps, mps_yerr, kill_restart, kill_restart_yerr = data
    pipeswitch_yerr = np.array(pipeswitch_yerr).T
    mps_yerr = np.array(mps_yerr).T
    kill_restart_yerr = np.array(kill_restart_yerr).T
    lower_bound = ready_model[3]

    x = np.arange(len(intervals))
    width = 0.8
    n = 4

    # setup font size
    font_size = 18
    plt.rc('font',**{'size': font_size, 'family': 'Arial' })
    plt.rc('pdf',fonttype = 42)

    # fig, ax = plt.subplots()
    fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 3.69),
                                gridspec_kw={'height_ratios': [1, 2]})
    plt.subplots_adjust(hspace=0.1)


    rects2 = ax.bar(x + width/n, kill_restart, width/n, label='Stop-and-start', 
                    yerr=kill_restart_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},linewidth=0.5,
                    edgecolor='black', color='tab:orange')

    rects3 = ax.bar(x , mps, width/n, label='MPS', 
                    yerr=mps_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},linewidth=0.5,
                    edgecolor='black',color='tab:green'
                )

    # upper part
    rects1 = ax.bar(x - width/n, pipeswitch, width/n, label=pipeswitch, 
                    yerr=pipeswitch_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},
                    edgecolor='black', linewidth=0.5, color='tab:blue'
                    )

    # bottom part
    rects2_2 = ax2.bar(x + width/n, kill_restart, width/n, label='Stop-and-start', 
                    yerr=kill_restart_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},linewidth=0.5,
                    edgecolor='black', color='tab:orange')

    rects2_3 = ax2.bar(x , mps, width/n, label='MPS', 
                    yerr=mps_yerr,
                    error_kw={'capsize':2, 'elinewidth':1}, linewidth=0.5,
                    edgecolor='black', color='tab:green')

    rects2_1 = ax2.bar(x - width/n, pipeswitch, width/n, label='PipeSwitch', 
                    yerr=pipeswitch_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},
                    edgecolor='black', linewidth=0.5,color='tab:blue'
                    )

    ax.set_ylim(6000, 10000)
    ax2.set_ylim(0, 450)

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
    ax.set_xticklabels(intervals)
    ax.legend([rects1, rects3, rects2], ['PipeSwitch', 'MPS', 'Stop-and-start'],
    # ax.legend([rects1, rects2], ['PipeSwitch', 'Stop-and-start'],
        frameon=False, ncol=2, loc='upper left',
            bbox_to_anchor=(0.0, 0.8, 0.5, 0.5),
            prop={'size': font_size-1})

    # fig.tight_layout()
    bar_size = 16
    offset=0.30

    ax2.axhline(lower_bound, ls='--', c='k')

    # kwargs = dict()
    # ax2.annotate('Lower bound', xy=(3.5, 31.15),  
    #             xytext=(3.3, 420),
    #             arrowprops=dict(facecolor='black', arrowstyle='-|>'),
    #             fontsize=13
    #             )

    # plt.show()
    plt.savefig(file_name, format="pdf")


def main():
    # Collect data with experiments
    data = collect_data()

    # Process data
    data_throughput = process_data_throughput(data)

    # Plot the figure
    plot_figure_throughput(data_throughput)

    # Process data
    data_latency = process_data_latency(data)

    # Plot the figure
    plot_figure_latency(data_latency)
    


if __name__ == '__main__':
    main()