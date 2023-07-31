#!bin/bash

#SBATCH --output=run_out.log
#SBATCH --error=run_error.log
#SBATCH --job-name=run

source ~/.bashrc                
conda activate pytorchenv       

qpython script.py