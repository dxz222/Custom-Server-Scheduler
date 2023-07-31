#!/bin/bash
source ~/.bashrc

for i in `seq 1 6`
do
	# Create job submission script.
    cmd=`sed -e "s/I/${i}/" dummy_job.sh`
    printf "${cmd}" > __job.sh
	
	# Submit script.
    sbatch __job.sh
	
	# Remove script.
    rm __job.sh
done
