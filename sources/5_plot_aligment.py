import os.path as op
from glob import glob
import mne

db_path = '/Users/fraimondo/data/insight/subjects'
subjects_dir = '/Users/fraimondo/data/insight/freesurfer'


broken = []

subjects = sorted([x.split('/')[-1] for x in glob(op.join(db_path, '*'))])

to_plot = [x for x in subjects
           if not op.exists(op.join(db_path, x, 'check.done')) and
           x not in broken]

print('Missing: {}'.format(len(to_plot)))
subject = to_plot[0]

print('Plotting {}'.format(subject))

montage = mne.channels.read_montage('GSN-HydroCel-256', unit='cm')

ch_names = montage.ch_names
ch_types = ['eeg'] * len(ch_names)
sfreq = 250
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types,
                       montage=montage)

trans_path = op.join(db_path, subject, '*-trans.fif')
trans_fname = glob(trans_path)[0]

mne.viz.plot_alignment(info, trans_fname, subject=subject, dig=True,
                       eeg='projected', subjects_dir=subjects_dir,
                       coord_frame='mri', surfaces=['head-dense', 'brain', 
                                                    'outer_skull'])

with open(op.join(db_path, subject, 'check.done'), 'w') as f:
    f.write('done')