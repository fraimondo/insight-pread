#!/bin/zsh
#
SUBJECTS_DIR=/Users/fraimondo/data/insight/freesurfer

b=()
for s in $SUBJECTS_DIR/*
do
	b+=(${s:t})
done

parallel -j1 --joblog job-inverse.log --resume --resume-failed --tag python 7_compute_inverse_s.py --subject {} ::: $b
