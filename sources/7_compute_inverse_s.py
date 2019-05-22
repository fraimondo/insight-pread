import os.path as op
from glob import glob
import mne

from argparse import ArgumentParser

parser = ArgumentParser(
    description='Computer inverse solution on the selected subject')

parser.add_argument('--subject', metavar='subject', nargs=1, type=str,
                    help='Subject name', required=True)

args = parser.parse_args()
subject = args.subject
if isinstance(subject, list):
    subject = subject[0]


db_path = '/Users/fraimondo/data/insight/'
subjects_dir = '/Users/fraimondo/data/insight/freesurfer'

trans_path = op.join(db_path, 'subjects', subject, '*-trans.fif')
trans_fname = glob(trans_path)[0]

raw_path = op.join(db_path, 'subjects', subject, '*-raw.fif')
raw_fname = glob(raw_path)[0]

fwd_fname = raw_fname.replace('-raw.fif', '-fwd.fif')
inv_fname = raw_fname.replace('-raw.fif', '-inv.fif')
epo_fname = raw_fname.replace('-raw.fif', '-epo.fif')

fwd = mne.read_forward_solution(fwd_fname)

epochs = mne.read_epochs(epo_fname)

noise_cov = mne.compute_covariance(epochs, tmax=0, method='auto',
                                   rank=None)

inverse_operator = mne.minimum_norm.make_inverse_operator(
    epochs.info, fwd, noise_cov, loose=0.2, depth=0.8)

mne.minimum_norm.write_inverse_operator(inv_fname, inverse_operator)

