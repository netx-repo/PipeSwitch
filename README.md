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

# 4. Contact

If you have any question, please contact `zbai1 at jhu dot edu`