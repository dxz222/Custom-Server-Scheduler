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

    def loop_monitor(self):
        available_gpus = []
        while True:
            gpu_dict = self.get_gpu_info()
            for i, (gpu_state, gpu_power, gpu_memory) in gpu_dict.items():
                if gpu_state == "P8" and gpu_power <= 25 and gpu_memory <= 5:  # 设置GPU选用条件，当前适配的是Nvidia-RTX3090
                    gpu_str = f"GPU/id: {i}, GPU/state: {gpu_state}, GPU/memory: {gpu_memory}MiB, GPU/power: {gpu_power}W\n"
                    sys.stdout.write(gpu_str)
                    sys.stdout.flush()
                    available_gpus.append(i)
            if len(available_gpus) >= self.min_gpu_number:
                return available_gpus
            else:
                available_gpus = []
                time.sleep(self.time_interval)

    def run(self, cmd):
        available_gpus = self.loop_monitor()
        gpu_list_str = ",".join(map(str, available_gpus))
        # 构建终端命令
        cmd = fr"NUM_GPUS={len(available_gpus)}; CUDA_VISIBLE_DEVICES={gpu_list_str} {cmd}"
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    min_gpu_number = 1  # 最小GPU数量，多于这个数值才会开始执行训练任务。
    time_interval = 10  # 监控GPU状态的频率，单位秒。
    gpu_get = GPUGet(min_gpu_number, time_interval)
    gpu_get.run('python '+' '.join(sys.argv[1:]))