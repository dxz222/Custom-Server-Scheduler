#!bin/bash
#SBATCH --account=dxz2019
#SBATCH --output=data/job_out_eval_VAR_I_VAR_J_VAR_K.log
#SBATCH --error=data/job_err_eval_VAR_I_VAR_J_VAR_K.log
#SBATCH --job-name=job_eval_VAR_I_VAR_J_VAR_K
#SBATCH --time=00:06:00         # Currently useless.

source ~/.bashrc
conda activate py3_8env

date

qpython test.py VAR_I VAR_J VAR_K

date
