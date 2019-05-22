#!/bin/zsh
#
SUBJECTS_DIR=/media/data/insight/subjects

b=()
for s in $SUBJECTS_DIR/*/*-src-epo.fif
do
	b+=(${${s:h}:t})
done

parallel -j1 --joblog job-EC.log --resume --resume-failed --tag python 9_compute_mrk_sources.py --subject {} --condition='EC' ::: $b
parallel -j1 --joblog job-EO.log --resume --resume-failed --tag python 9_compute_mrk_sources.py --subject {} --condition='EO' ::: $b
