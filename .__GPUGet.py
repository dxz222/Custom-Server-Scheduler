#! /usr/bin/python3
import os
import time
import sys
import fcntl

user_home = os.path.expanduser('~')

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

            """ 
            01 设置GPU可用的判断标准：
            通过nvidia-smi查看空闲时GPU的功率以及内存情况来加以更改

            参数：
                gpu_state: GPU性能
                gpu_power: GPU功率. 只有GPU功率低于此值才能被选为可用GPU
                gpu_memory: GPU内存. 只有GPU内存低于此值才能被选为可用GPU
            """
            if gpu_state == "P8" and gpu_power <= 25 and gpu_memory <= 5:  # 设置GPU选用条件，当前适配的是Nvidia-RTX2080 Ti
                gpu_str = f"GPU/id: {i}, GPU/state: {gpu_state}, GPU/memory: {gpu_memory}MiB, GPU/power: {gpu_power}W\n"
                sys.stdout.write(gpu_str)
                sys.stdout.flush()
                available_gpus.append(i)
        
        return available_gpus

    def loop_monitor(self):
        
        while True:
            available_gpus = self.get_available_gpus()
            
            # 获取通过记录的得到的可用GPU。
            with open(user_home + '/.gpu_status_file.info', 'r') as f:
                gpu_state_file = f.read().strip().split(' ')
                
                """ 
                02 设置GPU总数
                设置`range(n)`中n为机器中GPU总数  
                """
                gpu_state_file = [i for i in range(6) if gpu_state_file[i] == '0']

            # 综合得到的最终可用GPU。
            available_gpus = list(set(available_gpus).intersection(set(gpu_state_file)))

            if len(available_gpus) >= self.min_gpu_number:

                # 将用掉的GPU从记录中删除。
                with open(user_home + '/.gpu_status_file.info', 'r') as f:
                    gpu_state_file = f.read().strip().split(' ')
                
                with open(user_home + '/.gpu_status_file.info', 'w') as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    for i in available_gpus[:min_gpu_number]:
                        gpu_state_file[i] = 1
                    f.write(' '.join(list(map(str, gpu_state_file))))
                    fcntl.flock(f, fcntl.LOCK_UN)

                return available_gpus[:min_gpu_number]
            else:
                available_gpus = []
                time.sleep(self.time_interval)

    def regular_update_gpu(self):
        
        """ 
        02 设置GPU总数
        设置`[1,...,1]`中1的个数与机器中GPU总数一致  
        """
        gpu_state_file = [1,1,1,1,1,1]        
        
        while True:
            print(' ')
            os.system("date")
            available_gpus = self.get_available_gpus()
            
            # 将更新信息GPU状态文档。
            for i in available_gpus:
                gpu_state_file[i] = 0

            with open(user_home + '/.gpu_status_file.info', 'w') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(' '.join(list(map(str, gpu_state_file))))
                fcntl.flock(f, fcntl.LOCK_UN)
            
            time.sleep(6)


    def run(self, cmd):
        available_gpus = self.loop_monitor()
        gpu_list_str = ",".join(map(str, available_gpus))
        # 构建终端命令
        cmd = fr"NUM_GPUS={len(available_gpus)}; CUDA_VISIBLE_DEVICES={gpu_list_str} {cmd}"
        print(cmd)
        os.system(cmd)

        # 将用完的GPU在记录中还原。
        with open(user_home + '/.gpu_status_file.info', 'r') as f:
            gpu_state_file = f.read().strip().split(' ')
        
        with open(user_home + '/.gpu_status_file.info', 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            for i in available_gpus:
                gpu_state_file[i] = 0
            f.write(' '.join(list(map(str, gpu_state_file))))
            fcntl.flock(f, fcntl.LOCK_UN)


if __name__ == '__main__':
    min_gpu_number = 1  # 最小GPU数量，多于等于这个数值才会开始执行训练任务。
    time_interval = 5  # 监控GPU状态的频率，单位秒。
    gpu_get = GPUGet(min_gpu_number, time_interval)
    
    if len(sys.argv)==2 and sys.argv[1] == '0':  
        gpu_get.regular_update_gpu()
    else:
        gpu_get.run('python '+' '.join(sys.argv[1:]))
