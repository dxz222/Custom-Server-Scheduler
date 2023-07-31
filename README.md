# Custom Server Setting
## Introduction
This repository contains the document and auxiliary code for novice on high-throughput computation on small server, including the brief intro on shell usage, baisc configuration on environment, and multi-batch tasks setting for high-throughput computing. The PDF file will guide you through the first two cases, while the following will lead to you the last case.

## Feature
- **Queuing Mechanics:** Queue submitted computing missions up if there are no GPU for use. 
- **Dynamical Resourse Assignment:** Dynamically distribute the available GPU resoureces to queuing mission.
- With this plug-in, you can let the code run by itself at night.
- Also, it could ease your high-throughput computing missions with simple scripts.

## Dependency
- screen
- Nvidia GPU supporting `nvidia-smi` command.

## Configuration
1. Copy the file `.gpu_status_file.info`, `.__sbatch.sh` and`.__GPUGet.py` files into your home directory. The file `.gpu_status_file.info` contains the information for usability of GPU, where 0 represents free and 1 means occupied. Change the number of 0s in `.gpu_status_file.info` to the number of GPUs on your server.
2. Change some info in `.__GPUGet.py` according to the comments based on GPUs info on your machine.
3. Copy the code inside `more_than_bashrc.sh` at the end of your `.bashrc` file. Take care that do not change the original code in your `.bashrc` file.

## Usage
### Single-batch Submission
For single-batch mission, you could submit mission with the bash file like `run.sh`.

```bash
#!bin/bash

#SBATCH --output=run_out.log
#SBATCH --error=run_error.log
#SBATCH --job-name=run

qpython script.py
```
- `output`: the output file containing screening information.
- `error`: the error file containing error and warning messages.
- `job-name`: name of the submitted job.


### Multi-batch Submission
2. For multi-batch mission, you could submit mission with the bash files like `multi_run.sh` and `runs.sh`.

### GPU Info Update
3. You can refer to `multi_batch_GPU_test` for further demonstration.

## Alert
These codes are used for the server without sbatch plug-in installed. If you are using a cluster or server with sbatch plug-in, these codes will be incompatible with it thus cause some errors.
