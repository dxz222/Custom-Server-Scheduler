#!bin/bash
#SBATCH --account=dxz
#SBATCH --output=data/run_out.log
#SBATCH --error=data/run_error.log
#SBATCH --job-name=run

python script.py
