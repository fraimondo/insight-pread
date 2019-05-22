#!/bin/zsh
#
SUBJECTS_DIR=/Users/fraimondo/data/insight/freesurfer

b=()
for s in $SUBJECTS_DIR/*
do
	b+=(${s:t})
done

parallel -j1 --joblog job-labels.log --resume --resume-failed --tag python 8_extract_labels_s.py --subject {} ::: $b
