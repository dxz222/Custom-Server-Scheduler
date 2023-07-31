#! /usr/bin/python3
import os
import time
import sys


class GPUGet:
    def __init__(self,
                 min_gpu_number,
                 time_interval):
        self.min_gpu_number = min_gpu_number
        self.time_interval = time_interval

    def get_gpu_info(self):
        gpu_status = os.popen('nvidia-smi | grep %').read().strip().split('\n')
        gpu_dict = dict()
        for index in range(len(gpu_status)):
            gpu_state = str(gpu_status[index].strip('|').split('|')[0].split('   ')[2].strip())
            gpu_power = int(gpu_status[index].strip('|').split('|')[0].split('   ')[-1].split('/')[0].split('W')[0].strip())
            gpu_memory = int(gpu_status[index].strip('|').split('|')[1].split('/')[0].split('M')[0].strip())
            gpu_dict[index] = (gpu_state, gpu_power, gpu_memory)
        return gpu_dict
    
    def get_available_gpus(self):
        
        available_gpus = []
        gpu_dict = self.get_gpu_info()

        # 获取通过搜索的得到的可用GPU。
        for i, (gpu_state, gpu_power, gpu_memory) in gpu_dict.items():
            if gpu_state == "P8" and gpu_power <= 25 and gpu_memory <= 5:  # 设置GPU选用条件，当前适配的是Nvidia-RTX3090
                gpu_str = f"GPU/id: {i}, GPU/state: {gpu_state}, GPU/memory: {gpu_memory}MiB, GPU/power: {gpu_power}W\n"
                sys.stdout.write(gpu_str)
                sys.stdout.flush()
                available_gpus.append(i)
        
        return available_gpus

    def loop_monitor(self):
        
        while True:
            available_gpus = self.get_available_gpus()
            
            # 获取通过记录的得到的可用GPU。
            with open('/home/xzdai/.gpu_status_file.info', 'r') as f:
                gpu_state_file = f.read().strip().split(' ')
                gpu_state_file = [i for i in range(4) if gpu_state_file[i] == '0']

            # 综合得到的最终可用GPU。
            available_gpus = list(set(available_gpus).intersection(set(gpu_state_file)))

            if len(available_gpus) >= self.min_gpu_number:

                # 将用掉的GPU从记录中删除。
                with open('/home/xzdai/.gpu_status_file.info', 'r') as f:
                    gpu_state_file = f.read().strip().split(' ')
                
                with open('/home/xzdai/.gpu_status_file.info', 'w') as f:
                    for i in available_gpus[:min_gpu_number]:
                        gpu_state_file[i] = 1
                    f.write(' '.join(list(map(str, gpu_state_file))))

                return available_gpus[:min_gpu_number]
            else:
                available_gpus = []
                time.sleep(self.time_interval)

    def regular_update_gpu(self):
        gpu_state_file = [1,1,1,1]
        
        while True:
            print(' ')
            os.system("date")
            available_gpus = self.get_available_gpus()
            
            # 将更新信息GPU状态文档。
            for i in available_gpus:
                gpu_state_file[i] = 0

            with open('/home/xzdai/.gpu_status_file.info', 'w') as f:
                f.write(' '.join(list(map(str, gpu_state_file))))
            
            time.sleep(6)


    def run(self, cmd):
        available_gpus = self.loop_monitor()
        gpu_list_str = ",".join(map(str, available_gpus))
        # 构建终端命令
        cmd = fr"NUM_GPUS={len(available_gpus)}; CUDA_VISIBLE_DEVICES={gpu_list_str} {cmd}"
        print(cmd)
        os.system(cmd)

        # 将用完的GPU在记录中还原。
        with open('/home/xzdai/.gpu_status_file.info', 'r') as f:
            gpu_state_file = f.read().strip().split(' ')
        
        with open('/home/xzdai/.gpu_status_file.info', 'w') as f:
            for i in available_gpus:
                gpu_state_file[i] = 0
            f.write(' '.join(list(map(str, gpu_state_file))))


if __name__ == '__main__':
    min_gpu_number = 1  # 最小GPU数量，多于等于这个数值才会开始执行训练任务。
    time_interval = 5  # 监控GPU状态的频率，单位秒。
    gpu_get = GPUGet(min_gpu_number, time_interval)
    
    if len(sys.argv)==2 and sys.argv[1] == '0':  
        gpu_get.regular_update_gpu()
    else:
        gpu_get.run('python '+' '.join(sys.argv[1:]))
