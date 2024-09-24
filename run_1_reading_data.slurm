#!/bin/bash -l 

#SBATCH -t 23:59:59
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --account=intro_vsc36511
#SBATCH --cluster=genius
#SBATCH --mail-type FAIL,BEGIN,END
#SBATCH --job-name=run_pylis_read
#SBATCH --mail-user martinanatali@cnr.it
#SBATCH --output=./sbatch_out_files/%x.%j.out  #  Output file name with Job ID
#SBATCH --mem-per-cpu=3400
#SBATCH -o ./log/1_reading_data.txt
#SBATCH -e ./log/1_reading_data_out.txt 

####
# for more later lis simulations that use more than 6 cores you should add #SBATCH --exclude=r23i13n23

## command lines to load modules
module load cluster/genius/batch

source /data/leuven/365/vsc36511/WORK_AREA/CODING/pylis/conda/pylis_env_settings
python 1_reading_data.py