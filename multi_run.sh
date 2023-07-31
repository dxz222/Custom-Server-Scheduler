#!bin/bash

#SBATCH --output=run_out_I.log
#SBATCH --error=run_error_I.log
#SBATCH --job-name=run_I

source ~/.bashrc                
conda activate pytorchenv       

qpython script.py I