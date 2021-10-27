# 1. Introduction

This repository contains the source code for our OSDI'20 paper
["PipeSwitch: Fast Pipelined Context Switching for Deep Learning Applications"](https://www.usenix.org/conference/osdi20/presentation/bai). In addition, it contains some codes for systems which are compared with our system.

# 2. Contents

- [PipeSwitch](https://github.com/netx-repo/PipeSwitch/tree/main/pipeswitch): Our proposed system.
- [Ready model](https://github.com/netx-repo/PipeSwitch/tree/main/ready_model): The process with the required model is already loaded in the GPU. This solution provides the lower bound, which is the lowest latency we can achieve for an inference task.
- [Kill and restart](https://github.com/netx-repo/PipeSwitch/tree/main/kill_restart): It stops the training task in the GPU, and then starts the inference task.
- [PyTorch plugins](https://github.com/netx-repo/PipeSwitch/tree/main/pytorch_plugin): Modified PyTorch files, which are necessary for running PipeSwitch.
- [Tasks](https://github.com/netx-repo/PipeSwitch/tree/main/task): Models used for our evaluations.
- [Util](https://github.com/netx-repo/PipeSwitch/tree/main/util): Some common functions. For example, establishing TCP connections.
- [Clients](https://github.com/netx-repo/PipeSwitch/tree/main/client): Clients for sending requests.

# 3. Brief usage

0. Compile PyTorch for PipeSwitch. Ready-model and kill-and-restart could use original PyTorch.
1. Start the server you are interested, which can be PipeSwitch, ready-model or kill-and-restart.
2. Start the client to send requests.

More details are included in README under folders for each system.

# 4. Scripts to reproduce figures in our paper.

For the convenience, we implemented some scripts to reproduce our results reported in our paper.
We assume that you are using a host machine to do experiments in a remote server.
Thus, before using our scripts, you need to configure passwordless ssh access to the remote server.
We also expect you install python and docker on both the host and the remote machine.
By default, we use a server with NVIDIA V100 GPU with 16G GPU memory, such as AWS EC2 p3.2xlarge instances.

After you have configured the remote server, you need to add its IP address and host name in the file ```scripts/config/server.txt```.
Then you can run the script ```scripts/experiment.sh``` and wait for the result.

```scripts/experiment.sh``` will do the following things:
- Create a docker image with compiled PyTorch locally.
- Export the docker image to a file.
- Load the image file from the host machine to the remote server.
- Import the image file on the remote server.
- Create different docker images for different experiments on the remote server based on the basic image.
- Run experiments for figure 5-9.

You could modify the script to adapt to your requirement.
For example, you can compile PyTorch and create the basic docker image directly on the remote server.

We use different branches for different points in the figures.
These branches are now in Zhihao's repo, and we will move them to this repo in the future.

# 5. Contact

If you have any question, please contact `zbai1 at jhu dot edu`