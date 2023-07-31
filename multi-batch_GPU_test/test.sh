#!bin/bash
source ~/.bashrc
conda activate py3_8env

# Loop over image centers.
for i in `seq 0 1`
do
    # Loop over image masks.
    for j in `seq 0 1`
    do
        # Loop over shells.
        for k in `seq 0 1`
        do
            # Create job submission script, submit it, and clean.
            cmd=`sed -e "s/VAR_I/${i}/" -e "s/VAR_J/${j}/" -e "s/VAR_K/${k}/" dummy_task.sh`
            printf "${cmd}" > __job.sh
            sbatch __job.sh
            rm __job.sh
        done   
    done
done
