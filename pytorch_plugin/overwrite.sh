PYTORCH_PATH=$1

cp __init__.py $PYTORCH_PATH/torch/cuda/__init__.py
cp Module.cpp $PYTORCH_PATH/torch/csrc/cuda/Module.cpp
cp CUDACachingAllocator.h $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.h
cp CUDACachingAllocator.cpp $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.cpp