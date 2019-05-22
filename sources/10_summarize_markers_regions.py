import os
import os.path as op
from glob import glob
import mne
import nice
import pandas as pd
import json
from collections import OrderedDict
import numpy as np

from argparse import ArgumentParser

db_path = '/media/data/insight/'
conditions = ['EC', 'EO']

parser = ArgumentParser(
    description='Summarize markers on the selected subject')

parser.add_argument('--subject', metavar='subject', nargs=1, type=str,
                    help='Subject name', required=True)

args = parser.parse_args()
subject = args.subject
if isinstance(subject, list):
    subject = subject[0]


markers = {
    'wsmi_theta': 'nice/marker/SymbolicMutualInformation/theta_weighted',
    'wsmi_alpha': 'nice/marker/SymbolicMutualInformation/alpha_weighted',
    'wpli_theta': 'nice_sandbox/marker/WeightedPhaseLagIndex/theta_weighted',
    'wpli_alpha': 'nice_sandbox/marker/WeightedPhaseLagIndex/alpha_weighted',
    'plv_theta': 'nice_sandbox/marker/PhaseLockingValue/theta',
    'plv_alpha': 'nice_sandbox/marker/PhaseLockingValue/alpha',
}

df_data = {}
df_data['regions'] = []
df_data['condition'] = []

for k in markers.keys():
    df_data[k] = []

o_path = op.join(db_path, 'results', 'sources')
o_path = op.join(o_path, subject)

with open('../data/rois.json', 'r') as f:
    rois = json.load(f)

for condition in conditions:
    print('Using condition: {}'.format(condition))
    t_path = op.join(o_path, condition)

    fc = nice.read_markers(op.join(t_path, 'results-markers.hdf5'))
    _samp = fc['nice/marker/SymbolicMutualInformation/theta_weighted']
    labels = _samp.ch_info_['ch_names']
    rois_idx = OrderedDict()
    for roi, ch_names in rois.items():
        t_elems = np.array([labels.index(x) for x in ch_names])
        rois_idx[roi] = t_elems
    n_rois = len(rois_idx)
    rois_names = list(rois_idx.keys())

    for i in range(n_rois):
        i_roi = rois_names[i]
        i_idx = rois_idx[i_roi]
        for j in range(i, n_rois):
            j_roi = rois_names[j]
            j_idx = rois_idx[j_roi]
            r_name = '{}-{}'.format(i_roi, j_roi)
            df_data['regions'].append(r_name)

            for m_key, nice_marker in markers.items():
                marker_data = fc[nice_marker].data_
                if 'epochs' in fc[nice_marker]._axis_map:
                    marker_data = marker_data.mean(axis=-1)

                val = marker_data[i_idx, :][:, j_idx].mean(0).mean(0) 
                df_data[m_key].append(val)
            df_data['condition'].append(condition)

df = pd.DataFrame(df_data)

df.to_csv('./data/subjects/{}-markers.csv'.format(subject), sep=';')
