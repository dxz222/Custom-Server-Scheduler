""" Test file for the custom server scheduler """
""" Need the support of pytorch package """

import time
import torch
import sys

device = 'cuda' if torch.cuda.is_available() else 'cpu'

for i in range(10):
    a = torch.rand(1000,50000)
    b = torch.rand(50000,1000)
    a = a.to(device)    
    b = b.to(device)
    c = a@b
    time.sleep(3)

print(f'Done, {sys.argv[1]}, {sys.argv[2]}, {sys.argv[3]}')