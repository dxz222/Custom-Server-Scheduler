#!bin/bash
#SBATCH --account=dxz2019
#SBATCH --output=data/run.log
#SBATCH --error=data/run.log
#SBATCH --job-name=run

python script.py
