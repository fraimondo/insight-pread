#!/bin/bash

db_path=/media/data/insight
SUBJECTS_DIR=$db_path/freesurfer
subject=$1
echo $subject
dicom=`ls ${db_path}/mr/${subject}/T1/*.dic | head -n 1`
echo $dicom

recon-all -i $dicom -s $subject -sd $SUBJECTS_DIR -all

mri_annotation2label --subject $subject --hemi lh --sd $SUBJECTS_DIR --outdir $SUBJECTS_DIR/$subject/label/aparc/
mri_annotation2label --subject $subject --hemi rh --sd $SUBJECTS_DIR --outdir $SUBJECTS_DIR/$subject/label/aparc/