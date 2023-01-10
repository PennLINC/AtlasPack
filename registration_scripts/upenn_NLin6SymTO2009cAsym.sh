#!/bin/bash
#
#$ -N sym6to9casym 
#$ -pe threaded 16
#$ -l h_vmem=48G

SCRIPT_DIR=/cbica/projects/xcpDev/templateflow_collaboration/scripts
TEMPLATEFLOW_DIR=/cbica/projects/xcpDev/templateflow
WORK_DIR=/cbica/comp_space/xcpDev
DATA_DIR=/cbica/projects/xcpDev/templateflow_collaboration/data
SINGULARITY_IMG=/cbica/projects/xcpDev/templateflow_collaboration/code/tfreg_latest-2019-05-10-80289a40fca9.simg
REFSPACE=MNI152NLin6Asym
MOVSPACE=MNI152NLin2009cAsym
FS_RESULTS=/cbica/projects/xcpDev/templateflow_collaboration/data/derivatives/freesurfer_6.0.1
PARTICIPANTS=$( cat random_subs.txt )

export FS_LICENSE=${FREESURFER_HOME}/license.txt

singularity run \
    --cleanenv \
    -B $TEMPLATEFLOW_DIR:/opt/templateflow \
    -B $DATA_DIR:/data \
    -B $WORK_DIR:/work \
    -B $FS_RESULTS:/fs_results \
    $SINGULARITY_IMG \
        /data \
        --reference $REFSPACE \
        --moving $MOVSPACE \
        --cpu-count 16 \
        --omp-nthreads 8 \
        --participant-label $PARTICIPANTS \
        -vv -w /work/



echo Commandline: $cmd
eval $cmd
echo Finished
