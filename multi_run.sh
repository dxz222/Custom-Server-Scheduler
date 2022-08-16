#!bin/bash

#SBATCH --output=run_out_I.log
#SBATCH --error=run_error_I.log
#SBATCH --job-name=run_I

python script.py I
