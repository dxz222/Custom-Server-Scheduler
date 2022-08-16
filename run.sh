#!bin/bash
#SBATCH --account=dxz
#SBATCH --output=run_out.log
#SBATCH --error=run_error.log
#SBATCH --job-name=run

python script.py
