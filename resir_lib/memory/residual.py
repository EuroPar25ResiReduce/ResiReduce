from resir_lib import Memory
import sys
import re
import sys
import numpy as np
import os

class ResidualMemory(Memory):
    def __init__(self, beta=1.0, gamma=1.0):
        self.residuals = {}
        self.beta = beta
        self.gamma = gamma

    def compensate(self, tensor, name):
        """Update the tensor with the residuals."""
        if name in self.residuals:
            tensor = self.beta * self.residuals[name] + self.gamma * tensor
        return tensor

    def update(self, tensor, name, compressor, tensor_compressed, ctx):
        """Update the residuals."""
        # numel, shape = ctx
        # values, indices = tensor_compressed
        # if values.numel()!=numel:
        #     tensor_decompressed = compressor.decompress(tensor_compressed, ctx)
        # else:
        #     tensor_decompressed=values
        tensor_decompressed = compressor.decompress(tensor_compressed, ctx)
    
        residual = tensor - tensor_decompressed
        self.residuals[name] = residual
        
        return residual
    
    
    def print_ef(self, epoch, iter):
        
        print("len(self.residuals): ", len(self.residuals))

        for name, res in self.residuals.items():
            print("name: ", name, ", size: ", res.size(), ", numel: ", res.numel())
            
        total_memory_usage = 0
        for name, tensor in self.residuals.items():
            element_size = tensor.element_size()  # 每个元素占用的字节数
            numel = tensor.numel()  # 张量中元素的总数
            memory_usage = element_size * numel  # 张量占用的总字节数
            total_memory_usage += memory_usage
        print("Memory size: ", total_memory_usage, "B")
        print("Memory size: ", total_memory_usage / (1024 * 1024), "MB")
        print("Residuals size: ", sys.getsizeof(total_memory_usage), "B")



        print("OK!")

        return 1   






