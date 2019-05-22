import os
import os.path as op
import time
import mne
from mne.utils import logger
from nice_ext.api import utils, summarize_run
import pandas as pd

from argparse import ArgumentParser
import sys
import traceback

start_time = time.time()

parser = ArgumentParser(
    description='Extract topos')

parser.add_argument('--path', metavar='db_path', nargs=1, type=str,
                    help='Database path', required=True)

args = parser.parse_args()
db_path = args.path

if isinstance(db_path, list):
    db_path = db_path[0]

selected_fname = op.join(db_path, 'extra', 'id_INSIGHT_MEMENTO.csv')
df_map = pd.read_csv(selected_fname, sep=';')
df_map['MRI_ID'] = ['{}_{}'.format(x[:4], x[4:]) 
                    for x in df_map['id_MEMENTO']]
df_map['EEG_ID'] = ['M0_{}_{}'.format(x[:4], x[4:])
                    for x in df_map['id_INSIGHT']]

reductions=['aramis/insight/egi256/trim_mean80',
            'aramis/insight/egi256/std']

for condition in ['EC', 'EO']:
    results_dir = op.join(db_path, 'results', condition)
    summary = summarize_run(
        in_path=results_dir, recompute=False,
        reductions=reductions)
    summary = summary.filter(subjects=df_map['EEG_ID'].values)
 
    summary.save(op.join('data', 'summary', condition, 'all'))
    c_names = ['E{}'.format(x) for x in range(1, 257)]

    for this_reduction, this_topo in summary.topos().items():
        red_fname = this_reduction.split('/')[-1]
        for i_marker, marker in enumerate(summary._topo_names):
            fname = '_'.join(marker.split('/')[-2:])
            fname = '{}_{}.csv'.format(fname, red_fname)
            df = pd.DataFrame(this_topo[i_marker].T, columns=c_names, 
                              index=summary.subjects)
            df.to_csv(op.join('data', condition, fname), sep=';')