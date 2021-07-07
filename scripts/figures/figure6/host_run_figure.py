import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FLAG = 'OpenSourceOutputFlag'

systems = [
    'ready_model',
    'pipeswitch', 
    # 'mps', 
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
    for system in systems:
        data[system] = {}
        for interval in intervals:
            print ('Plot figure 6: %s, %s' % (system, interval))

            # Run the experiment
            result = subprocess.run(['bash', 'scripts/figures/figure6/%s_%s/host_run_data.sh' % (system, interval)], stdout=subprocess.PIPE)

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

def process_data_throughput(data):
    ret = []
    for system in systems:
        ret.append([])
        for interval in intervals:
            ret[-1].append(data[system][interval][0])
    return ret

def plot_figure_throughput(data):
    file_name = "output/figure6_throughput.pdf"

    # intervals = ['1s', '2s', '5s', '10s', '30s']

    # our_sys = [245.846,246.6133,247.2066,245.7919,245.137]
    # kill_restart = np.array([0.3, 0.23333333333333334, 0.16666666666666666, 10.96, 23.98]) * 8
    # mps = [98.5, 100.61999999999999, 102.16666666666666, 102.18799999999999, 103.79733333333334]
    # # unified_memory = [119.39333333333336, 140.99333333333334, 159.41333333333333, 165.61599999999999, 165.90133333333333]

    # ready_model, pipeswitch, mps, kill_restart = data
    ready_model, pipeswitch, kill_restart = data
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

    # rects3 = ax.bar(x , mps, width/n, label='MPS', linewidth=0.5,
    #                 edgecolor='black', color='tab:green')

    rects1 = ax.bar(x + width/n, pipeswitch, width/n, label='PipeSwitch', linewidth=0.5,
                    edgecolor='black', color='tab:blue')

    ax.set_ylabel('Throughput (batches/sec)')
    # ax.set_title('End to End Latency: vs Simple Transmission (V100)')
    ax.set_xticks(x)
    ax.set_xticklabels(intervals)
    # ax.legend([rects1, rects3, rects2], ['PipeSwitch', 'MPS', 'Stop-and-start'],
    ax.legend([rects1, rects2], ['PipeSwitch', 'Stop-and-start'],
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

    # our_sys = [32.310043029232766, 32.21757734471539, 
    #         32.145160522948565, 32.3249236662986, 
    #         32.40527434978599]

    # our_sys_yerr = np.array([[3.3161980432708518, 22.293772049502586], 
    #                         [3.1913074319956607, 22.96225702112934], 
    #                         [3.116983261596026, 31.895500335205732], 
    #                         [3.2702819426657896, 28.30778202217796], 
    #                         [3.41190620098228, 21.437508624457173]]).T

    # kill_restart = [6266.83055029975, 6294.484921864101, 6403.910398483276, 
    #                 90.95868490038127, 
    #                 41.426614552429726]

    # kill_restart_yerr = np.array([[32.84417258368558, 44.84523667229587], 
    #                             [35.6305326734273, 72.65584809439497], 
    #                             [30.942201614379883, 32.1042537689209], 
    #                             [61.331361749746506, 6468.853384038828], 
    #                             [11.640743046692421, 6495.63769933612]]).T

    # mps = [83.46177682053619, 79.29460095465164, 
    #     78.08835970830373, 78.07119123090264, 
    #     76.79601950055465]

    # mps_yerr = np.array([[51.24212845933013, 297.03], 
    #                     [43.49915074408035, 317.4272389501335],
    #                     [47.02814089726857, 317.5932599358613], 
    #                     [46.45140401471612, 318.1096769179011], 
    #                     [44.879877990544884, 326.2870665132393]]).T

    # pipeswitch, pipeswitch_err, mps, mps_err, kill_restart, kill_restart_err = data
    ready_model, ready_model_yerr, pipeswitch, pipeswitch_yerr, kill_restart, kill_restart_yerr = data
    pipeswitch_yerr = np.array(pipeswitch_yerr).T
    # mps_yerr = np.array(mps_yerr).T
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

    # rects3 = ax.bar(x , mps, width/n, label='MPS', 
    #                 yerr=mps_yerr,
    #                 error_kw={'capsize':2, 'elinewidth':1},linewidth=0.5,
    #                 edgecolor='black',color='tab:green'
    #             )

    # upper part
    rects1 = ax.bar(x - width/n, pipeswitch, width/n, label=pipeswitch, 
                    yerr=pipeswitch_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},
                    edgecolor='black', linewidth=0.5, color='tab:blue'
                    )


    # rects4 = ax.bar(x , unified_mem, width/n, label="Unified Memory",
    #                 yerr=unified_mem_yerr,
    #                 error_kw={'capsize':2, 'elinewidth':1},linewidth=0.5,
    #                 edgecolor='black')





    # bottom part
    rects2_2 = ax2.bar(x + width/n, kill_restart, width/n, label='Stop-and-start', 
                    yerr=kill_restart_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},linewidth=0.5,
                    edgecolor='black', color='tab:orange')

    # rects2_3 = ax2.bar(x , mps, width/n, label='MPS', 
    #                 yerr=mps_yerr,
    #                 error_kw={'capsize':2, 'elinewidth':1}, linewidth=0.5,
    #                 edgecolor='black', color='tab:green')

    rects2_1 = ax2.bar(x - width/n, pipeswitch, width/n, label='PipeSwitch', 
                    yerr=pipeswitch_yerr,
                    error_kw={'capsize':2, 'elinewidth':1},
                    edgecolor='black', linewidth=0.5,color='tab:blue'
                    )

    # rects2_4 = ax2.bar(x , unified_mem, width/n, label="Unified Memory",
    #                 yerr=unified_mem_yerr,
    #                 error_kw={'capsize':2, 'elinewidth':1}, linewidth=0.5,
    #                 edgecolor='black')




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
    # ax.legend([rects1, rects3, rects2], ['PipeSwitch', 'MPS', 'Stop-and-start'],
    ax.legend([rects1, rects2], ['PipeSwitch', 'Stop-and-start'],
        frameon=False, ncol=2, loc='upper left',
            bbox_to_anchor=(0.0, 0.8, 0.5, 0.5),
            prop={'size': font_size-1})

    # fig.tight_layout()
    bar_size = 16
    offset=0.30
    # upper_bar = 5600
    # lower_bar = 710
    # ax.text(offset, upper_bar, "/",rotation=-55, fontdict={'family': 'serif',
    #                                     'color':  'black',
    #                                     'weight': 'normal',
    #                                     'size': bar_size,
    #                                     })
    # ax2.text(offset, lower_bar, "/",rotation=-55, fontdict={'family': 'serif',
    #                                     'color':  'black',
    #                                     'weight': 'normal',
    #                                     'size': bar_size,
    #                                     })
    # ax.text(1+offset, upper_bar, "/",rotation=-55, fontdict={'family': 'serif',
    #                                     'color':  'black',
    #                                     'weight': 'normal',
    #                                     'size': bar_size,
    #                                     })
    # ax2.text(1+offset, lower_bar, "/",rotation=-55, fontdict={'family': 'serif',
    #                                     'color':  'black',
    #                                     'weight': 'normal',
    #                                     'size': bar_size,
    #                                     })
    # ax.text(2+offset, upper_bar, "/",rotation=-55, fontdict={'family': 'serif',
    #                                     'color':  'black',
    #                                     'weight': 'normal',
    #                                     'size': bar_size,
    #                                     })
    # ax2.text(2+offset, lower_bar, "/",rotation=-55, fontdict={'family': 'serif',
    #                                     'color':  'black',
    #                                     'weight': 'normal',
    #                                     'size': bar_size,
    #                                     })


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
    # data = collect_data()
    data = {'ready_model': {'1s': [28.8, 35.48775530523724, 34.409284591674805, 38.29383850097656], '2s': [28.3, 35.46297128967177, 34.41166877746582, 38.6662483215332], '5s': [26.4, 37.74152018807151, 35.96091270446777, 106.89425468444824], '10s': [26.619999999999997, 37.41094243875757, 34.615516662597656, 136.85202598571777], '30s': [27.233333333333334, 36.540557617364925, 35.143375396728516, 48.157691955566406]}, 'pipeswitch': {'1s': [0.0, 39.16411492431048, 37.07551956176758, 50.66847801208496], '2s': [0.0, 36.7473935427731, 34.81578826904297, 48.90275001525879], '5s': [0.0, 37.757791352994516, 35.680294036865234, 51.213979721069336], '10s': [0.0, 38.10940678610186, 36.34953498840332, 50.12845993041992], '30s': [0.0, 38.612402064128986, 36.35883331298828, 133.84366035461426]}, 'kill_restart': {'1s': [28.6, 35.318364630212315, 33.98561477661133, 44.42262649536133], '2s': [28.5, 35.25834460007517, 34.430742263793945, 38.03443908691406], '5s': [28.660000000000004, 34.81583735032757, 33.51235389709473, 38.49530220031738], '10s': [27.5, 36.22256010228937, 34.77311134338379, 47.37210273742676], '30s': [27.513333333333332, 36.15405370630477, 33.809661865234375, 141.4775848388672]}}
    print (data)

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