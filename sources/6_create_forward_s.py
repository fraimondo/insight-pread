import os.path as op
from glob import glob
import mne
import sys

from argparse import ArgumentParser

parser = ArgumentParser(
    description='Create forward model on the selected subject')

parser.add_argument('--subject', metavar='subject', nargs=1, type=str,
                    help='Subject name', required=True)

args = parser.parse_args()
subject = args.subject
if isinstance(subject, list):
    subject = subject[0]

db_path = '/Users/fraimondo/data/insight/'
subjects_dir = '/Users/fraimondo/data/insight/freesurfer'


trans_path = op.join(db_path, 'subjects', subject, '*-trans.fif')
trans_fname = glob(trans_path)
if len(trans_fname) != 1:
    print('No TRANS file.')
    sys.exit(-2)

trans_fname = trans_fname[0]

raw_path = op.join(db_path, 'subjects', subject, '*-raw.fif')
raw_fname = glob(raw_path)[0]


fwd_fname = raw_fname.replace('-raw.fif', '-fwd.fif')

info = mne.io.read_info(raw_fname)

src = mne.setup_source_space(subject, spacing='oct6',
                             subjects_dir=subjects_dir, add_dist=False)

conductivity = (0.3, 0.006, 0.3)  # for three layers
model = mne.make_bem_model(subject=subject, ico=4,
                           conductivity=conductivity,
                           subjects_dir=subjects_dir)
bem = mne.make_bem_solution(model)

fwd = mne.make_forward_solution(raw_fname, trans=trans_fname, src=src, bem=bem,
                                meg=False, eeg=True, mindist=5.0, n_jobs=2)
mne.write_forward_solution(fwd_fname, fwd, overwrite=True)