#!/bin/zsh
export SUBJECTS_DIR=/Users/fraimondo/data/insight/freesurfer
export PATH=$PATH:$MNE_ROOT/bin/:$MATLAB_ROOT/bin/
$MNE_ROOT/bin/mne_setup
$MNE_ROOT/bin/mne_setup_matlab_sh
export FREESURFER_HOME=/Applications/freesurfer/
. $FREESURFER_HOME/SetUpFreeSurfer.sh

mne_watershed_bem --subject $1 --overwrite
cd "${SUBJECTS_DIR}/${1}/bem"
ln -s watershed/*_outer_skin_surface outer_skin.surf
ln -s watershed/*_outer_skull_surface outer_skull.surf
ln -s watershed/*_inner_skull_surface inner_skull.surf
ln -s watershed/*_brain_surface brain.surf