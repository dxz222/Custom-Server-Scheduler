#!bin/bash
#SBATCH --output=run_out.log
#SBATCH --error=run_error.log
#SBATCH --job-name=run

python script.py
