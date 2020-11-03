# PyTorch plugins
This folder contains modifications to the PyTorch code.

# Content
- PyTorch files
    - \_\_init\_\_.py: $PYTORCH_PATH/torch/cuda/\_\_init\_\_.py
    - Module.cpp: $PYTORCH_PATH/torch/csrc/cuda/Module.cpp
    - CUDACachingAllocator.cpp: $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.cpp
    - CUDACachingAllocator.h: $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.h
- overwrite.sh: Overwrite corresponding files in $PYTORCH_PATH

# Usage
1. Compile the original PyTorch (1.3.0) from source. https://github.com/pytorch/pytorch/tree/v1.3.0.
2. Copy modified files to the PyTorch folder. `bash overwrite.sh [path_to_PyTorch]`
3. Compile the modified PyTorch. Then you may install it to Python library folder or set `PYTHONPATH` to make sure that PipeSwitch can find it.

# Implementation
The code is implemented for NVIDIA V100 and T4, both of which have 16 GB GPU memory. Thus, some related parameters for memory management are directly written in the code. If you use GPUs with different GPU memory size, you need to change these parameters.