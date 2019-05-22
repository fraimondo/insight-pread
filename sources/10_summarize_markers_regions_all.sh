#!/bin/zsh
#
SUBJECTS_DIR=/media/data/insight/results/sources

b=()
for s in $SUBJECTS_DIR/*
do
	b+=(${s:t})
done

parallel -j1 --joblog job-summarize.log --resume --resume-failed --tag python 10_summarize_markers_regions.py --subject {} ::: $b
