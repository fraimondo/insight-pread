#!/bin/zsh
#

db_path=/media/data/insight

b=()
for s in $db_path/mr/*
do
	b+=(${s:t})
done

echo $b
parallel -j40 --delay 10 --joblog job-freesurfer.log --resume --resume-failed --tag ./1_run_freesurfer_s.sh {} ::: $b