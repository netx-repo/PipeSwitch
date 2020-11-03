import importlib

import torch

### Class
class ModelSummary():
    def __init__(self, model_name, TERMINATE_SIGNAL,
                 param_trans_pipe):
        """ """
        self.model_name = model_name
        self.TERMINATE_SIGNAL = TERMINATE_SIGNAL
        self.param_trans_pipe = param_trans_pipe
        self.load_model()

    def execute(self, data_b):
        if data_b is None:
            return self.func(self.model, self.data_loader)
        else:
            return self.func(self.model, data_b)

    def reset_initialized(self, mod):
        if hasattr(mod, 'initialized'):
            mod.initialized = False
        for child in mod.children():
            self.reset_initialized(child)

    def insert_lock_hook(self, shape_summary_list):
        """ """
        for _, _, _, mod_sublist in shape_summary_list:
            mod = mod_sublist[0]
            mod.initialized = False
            def hook_wait_for_parameter_lock(mod, input):
                if not mod.initialized:
                    complete_name = self.param_trans_pipe.recv()
                    if complete_name != mod.fullname:
                        raise Exception('Invalid complete trans')
                    mod.initialized = True
            mod.register_forward_pre_hook(hook_wait_for_parameter_lock)

    def insert_terminate_hook(self, mod):
        """ """
        def hook_terminate(mod, input, output):
            torch.cuda.synchronize()
            if self.TERMINATE_SIGNAL[0] == 2:
                raise Exception('terminate signal received')
        if len(list(mod.children())) == 0:
            mod.register_forward_hook(hook_terminate)
            mod.register_backward_hook(hook_terminate)
        else:
            for child in mod.children():
                self.insert_terminate_hook(child)

    def load_model(self):
        model_module = importlib.import_module('task.' + self.model_name)
        self.model, self.func, self.shape_summary_list = model_module.import_task()
        self.data_loader = model_module.import_data_loader()

        # Eliminate parameters and buffers
        self.reset_initialized(self.model)

        # Insert locks for waiting parameters and add pre_formard_hook to wait for locks
        self.insert_lock_hook(self.shape_summary_list)

        # Add hooks for termination in both forward and backward propagations
        if 'training' in self.model_name:
            self.insert_terminate_hook(self.model)

        # Allocate fake memory for parameters
        self.cuda_stream_for_parameter = torch.cuda.Stream()
        self.cuda_stream_for_computation = torch.cuda.Stream()

        with torch.cuda.stream(self.cuda_stream_for_parameter):
            torch.cuda.insert_shared_cache_for_parameter()
        with torch.cuda.stream(self.cuda_stream_for_computation):
            torch.cuda.insert_shared_cache_for_computation()

        with torch.cuda.stream(self.cuda_stream_for_parameter):
            for shape_list, param_list, buf_list, _ in self.shape_summary_list:
                for shape, p in zip(shape_list[:len(param_list)], param_list):
                    p.data = torch.empty(shape, device='cuda')
                for shape, b in zip(shape_list[len(param_list):], buf_list):
                    mod, key = b
                    mod._buffers[key] = torch.empty(shape, device='cuda')

### Class End
