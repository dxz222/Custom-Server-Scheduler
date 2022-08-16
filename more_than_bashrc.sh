# Sbatch.
function sbatch () {
    
    # Missing arguments checks.
    if [ $# -lt 1 ]
    then
        echo "Missing argument(s)."
        return 1
    fi

     # Redundant arguments checks.
    if [ $# -gt 1 ]
    then
        echo "Too many argument(s)."
        return 1
    fi

    # Readout running information.
    account=`sed -n 's/#SBATCH --account=//p' $1`   # $1: file name.
    output=`sed -n 's/#SBATCH --output=//p' $1`
    error=`sed -n 's/#SBATCH --error=//p' $1`
    job_name=`sed -n 's/#SBATCH --job-name=//p' $1`
    time=`sed -n 's/#SBATCH --time=//p' $1`

    # Submit the mission in a new screen.
    screen -S ${job_name} -d -m bash ~/.__sbatch.sh $1 ${output} ${error}

    # Echo support information.
    echo "Submit job: ${job_name}."
}
