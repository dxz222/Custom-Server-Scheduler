# STEM Server Setting
## Introduction
This repository contains the codes for multi-batch running on server. 

## Dependency
- screen

## Usage
1. Copy the file `.__sbatch.sh` and `.__GPUGet.py` files into your home directory.
2. Copy the code inside `more_than_bashrc.sh` at the end of your `.bashrc` file. Take care that do not change the original code in your `.bashrc` file.
3. For single-batch mission, you could submit mission with the bash file like `run.sh`.
4. For multi-batch mission, you could submit mission with the bash files like `multi_run.sh` and 'runs.sh'.
5. You can refer to `multi_batch_GPU_test` for further demonstration.

## Alert
These codes are used for the server without sbatch plug-in installed. If you are using a cluster or server with sbatch plug-in, these codes will be incompatible with it thus cause some errors.
