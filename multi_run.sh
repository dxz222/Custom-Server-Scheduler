#!bin/bash
#SBATCH --account=dxz222
#SBATCH --output=data/run_out_I.log
#SBATCH --error=data/run_err_I.log
#SBATCH --job-name=run_I

python print.py VAR_I
