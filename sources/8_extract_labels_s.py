import os.path as op
from glob import glob
import numpy as np
import mne

sys.path.append('../')
from common import sources_labels


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


raw_path = op.join(db_path, 'subjects', subject, '*-raw.fif')
raw_fname = glob(raw_path)[0]

fwd_fname = raw_fname.replace('-raw.fif', '-fwd.fif')
inv_fname = raw_fname.replace('-raw.fif', '-inv.fif')
epo_fname = raw_fname.replace('-raw.fif', '-epo.fif')

inverse_operator = mne.minimum_norm.read_inverse_operator(inv_fname)
epochs = mne.read_epochs(epo_fname, preload=True)

snr = 3.0
lambda2 = 1.0 / snr ** 2
method = 'dSPM'

stcs = mne.minimum_norm.apply_inverse_epochs(
    epochs, inverse_operator, lambda2, method, pick_ori=None)


labels_fnames = [
    op.join(subjects_dir, subject, 'label', 'aparc', '{}.label'.format(label))
    for label in sources_labels]

labels = [mne.read_label(f) for f in labels_fnames]

src = inverse_operator['src']
mean_flip = [
    stc.extract_label_time_course(
        labels, src, mode='mean_flip', allow_empty=True)
    for stc in stcs]
src_data = np.array(mean_flip)

ch_names = sources_labels
sfreq = epochs.info['sfreq']
ch_types = 'eeg'
info = mne.create_info(ch_names, sfreq, ch_types)

src_epochs = mne.EpochsArray(
    data=src_data, info=info, events=epochs.events, tmin=epochs.tmin,
    event_id=epochs.event_id)

src_epo_fname = raw_fname.replace('-raw.fif', '-src-epo.fif')

src_epochs.save(src_epo_fname)