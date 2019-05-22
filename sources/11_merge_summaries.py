import os.path as op
from glob import glob
import pandas as pd

import numpy as np

metadata = pd.read_csv('data/donnees_tirees.csv', sep=';')
metadata['ID'] = ['M0_{}'.format(x.replace('-', '_')) 
                  for x in metadata['id_INSIGHT'].values]

fnames = [x for x in glob('./data/subjects/*-markers.csv')]

markers = [
    'wsmi_theta',
    'wsmi_alpha',
    'wpli_theta',
    'wpli_alpha',
    'plv_theta',
    'plv_alpha'
]

dfs = []

for fname in fnames:
    subject = fname.split('/')[-1][:12]
    if subject in metadata['ID'].values:
        df = pd.read_csv(fname, sep=';')
        df['ID'] = subject.strip()
        dfs.append(df)
df = pd.concat(dfs).set_index(['ID', 'regions', 'condition'])
df.columns.name = 'marker'

df = df[markers].stack()
df.name = 'value'

df = df.to_frame()  

metadata = metadata.set_index('ID')
columns = ['groupe', 'sexe', 'age_M0', 'apoe4', 'NSC_bin']
df = df.join(metadata[columns]).reset_index()

df.to_csv('data/all_values.csv', sep=';')