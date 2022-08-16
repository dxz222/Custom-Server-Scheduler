#!bin/bash
#SBATCH --account=dxz222
#SBATCH --output=data/run_out_I.log
#SBATCH --error=data/run_error_I.log
#SBATCH --job-name=run_I

python script.py I
