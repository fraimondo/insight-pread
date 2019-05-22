import mne
from glob import glob
import os.path as op
import pandas as pd
import sys

db_path = '/Users/fraimondo/data/insight'
subjects_dir = op.join(db_path, 'freesurfer')
eeg_dir = op.join(db_path, 'subjects')

selected_fname = op.join(db_path, 'extra', 'donnees_tirees.csv')
df = pd.read_csv(selected_fname, sep=';')
df['MRI_ID'] = ['{}_{}'.format(x[:4], x[4:]) for x in df['id_MEMENTO']]
df['EEG_ID'] = ['M0_{}'.format(x.replace('-', '_')) for x in df['id_INSIGHT']]


dirs = [x.split('/')[-1] for x in glob(op.join(eeg_dir, '*'))]

missing_eeg = [x for x in df['EEG_ID'] if x not in dirs]
if len(missing_eeg) > 0:
    print('MISSING EEGs!!!')
    sys.exit(-1)

fnames = [x.split('/')[-2] for x in glob(op.join(eeg_dir, '*/*-trans.fif'))]

missing = sorted([x for x in df['EEG_ID'].values if x not in fnames])
print(len(missing))
print(missing)

skip = [
    # 'M0_0033_SODO',  # waiting for freesurfer
]

missing = [x for x in missing if x not in skip]

if len(missing) > 0:
    subject = missing[0]

    fname = [x for x in glob(op.join(eeg_dir, subject, '*-raw.fif'))][0]
    print(fname)

    mne.gui.coregistration(
        subjects_dir=subjects_dir, guess_mri_subject=False,
        inst=fname,
        subject=subject)