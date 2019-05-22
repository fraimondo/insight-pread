#!/bin/zsh
#
export SUBJECTS_DIR=/Users/fraimondo/data/insight/freesurfer
export PATH=$PATH:$MNE_ROOT/bin/:$MATLAB_ROOT/bin/
$MNE_ROOT/bin/mne_setup
$MNE_ROOT/bin/mne_setup_matlab_sh
export FREESURFER_HOME=/Applications/freesurfer/
. $FREESURFER_HOME/SetUpFreeSurfer.sh


b=()
for s in $SUBJECTS_DIR/*
do
	b+=(${s:t})
done

parallel -j2 --joblog job-watershed.log --resume --resume-failed --tag ./3_create_watershed_bem_s.sh {}  ::: $b


