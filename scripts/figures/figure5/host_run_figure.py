import os

systems = ['ready_model', 'pipeswitch', 'mps', 'stop_and_start']
models = ['resnet152', 'inception_v3', 'bert_base']

def main():
    data = {}
    for system in systems:
        for model in models:
            os.system('bash scripts/figures/figure5/figure5_%s_%s/host_run_data.sh' % (system, model))
            # Get output
            # data[(system, model)] = output

    # Plot the figure

if __name__ == '__main__':
    main()