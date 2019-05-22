#!/bin/zsh
#
SUBJECTS_DIR=/Users/fraimondo/data/insight/freesurfer

b=()
for s in $SUBJECTS_DIR/*
do
	b+=(${s:t})
done

parallel -j1 --joblog job-forward.log --resume --resume-failed --tag python 6_create_forward_s.py --subject {} ::: $b
