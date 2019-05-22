#!/bin/zsh
#
SUBJECTS_DIR=/media/data/insight/subjects

b=()
for s in $SUBJECTS_DIR/*
do
	b+=(${s:t})
done

parallel -j10 --joblog job-markers.log --resume --resume-failed --tag python 1_compute_eeg_markers_s.py --path=/media/data/insight --subject {} ::: $b
