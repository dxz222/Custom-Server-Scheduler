#!/bin/bash
source ~/.bashrc

for i in `seq 1 6`
do
    # Create job submission script.
    cmd=`sed -e "s/VAR_I/${i}/" dummy_job.sh`
    printf "${cmd}" > __job.sh
	
	# Submit script.
    sbatch __job.sh
    sleep 0.1	# Wait for a while for submitting.
	
	# Remove script.
    rm __job.sh
done
