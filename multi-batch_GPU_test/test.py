# import configparser
# import os
# import subprocess
import time
# from multiprocessing import Pool
# import json

# ################################################################################
# # Functions.
# ################################################################################

# def task_initialization(config_path):
    
#     config = configparser.ConfigParser()
#     config.read(config_path)
#     python_files = eval(config['BATCH']['python_files'])
    
#     return python_files


# def gpu_update(GPUs):

#     gpu_index, gpu_memory = zip(*get_gpu_status())

#     GPUs = [GPUs[i] for i in range(len(gpu_index)) if gpu_memory[i] < memory_threshold]

#     return GPUs

# def task_update():

#     pass

#     return None

# def gpu_initialization(config_path):

#     config = configparser.ConfigParser()
#     config.read(config_path)
#     num_gpus = int(config['GPU']['num_gpus'])
#     memory_threshold = float(config['GPU']['memory_threshold'])

#     return num_gpus, memory_threshold

# def get_available_gpu(GPUs):

#     avai_GPUs = [i for i in range(len(GPUs)) if GPUs[i] != 0]

#     if avai_GPUs == []:             # Not availabel.
#         return -1
#     else:
#         gpu_index = avai_GPUs[0]
#         return gpu_index

# def get_queuing_task(Quening_Tasks):

#     if Quening_Tasks == []:        # All set.
#         return -1
#     else:
#         task = list(Quening_Tasks.items())[0]
#         return task

# def task_submission(tasks, gpu_index):
    
#     os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_index)

#     # poll.apply_async(subprocess.check_output)

#     return None

# def get_gpu_status():
    
#     output = subprocess.check_output("nvidia-smi --query-gpu=index,utilization.memory --format=csv,noheader", shell=True).decode('utf-8')
#     gpu_status = [line.strip('%').split(',') for line in output.strip().split('\n')]
#     gpu_status = [(int(gpu), int(memory)) for gpu, memory in gpu_status]
#     return gpu_status

# def monitor():

#     pass

#     return None

# def delete_task(Tasks, name):

#     del Tasks[name]

#     return None



# if __name__ == '__main__':

#     # GPU initialization.
#     config_path = 'config.ini'
#     num_gpu, memory_threshold = gpu_initialization(config_path)
#     GPUs = [1]*num_gpu
#     GPUs = gpu_update(GPUs)

#     # Task initialization.
#     Tasks = task_initialization(config_path)

#     # Initialize pool.
#     pool = Pool(processes=num_gpu)
#     Quening_Tasks = Tasks.copy()

#     # 
#     task = get_queuing_task(Quening_Tasks)

#     if task != -1:
#         gpu_index = get_available_gpu(GPUs)
    
#         if gpu_index != -1:
#             task_submission(task, gpu_index)
        
#         else:
#             time.sleep(30)

#     else:               # No more queuing task.
#         poll.close()
#         poll.join()
    
#     print('All Tasks Finished!')

#     # while len(Tasks):
        


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

print(f'Done, {sys.argv[0]}, {sys.argv[1]}, {sys.argv[2]}')