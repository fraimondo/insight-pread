import os
import os.path as op
from glob import glob
import mne

from argparse import ArgumentParser
import sys
sys.path.append('../')
from common import get_src_markers, get_src_reductions


parser = ArgumentParser(
    description='Computer inverse solution on the selected subject')

parser.add_argument('--subject', metavar='subject', nargs=1, type=str,
                    help='Subject name', required=True)

parser.add_argument('--condition', metavar='condition', nargs=1, type=str,
                    help='Condition [EO, EC]', required=True)

args = parser.parse_args()
subject = args.subject
condition = args.condition
if isinstance(subject, list):
    subject = subject[0]

if isinstance(condition, list):
    condition = condition[0]

if condition not in ['EC', 'EO']:
    raise ValueError('wrong condition')

print('Using only condition {}'.format(condition))

db_path = '/media/data/insight/'

s_dir = op.join(db_path, 'subjects')
t_s_dir = op.join(s_dir, subject)
fnames = [x for x in glob(
    op.join(t_s_dir, '*aramis-insight-egi-src-epo.fif'))]
epochs = mne.read_epochs(fnames[0], preload=True, verbose=True)

epochs = epochs[condition]
print(epochs)

fc = get_src_markers()
fc.fit(epochs)

o_path = op.join(db_path, 'results')
if not op.exists(o_path):
    os.mkdir(o_path)

o_path = op.join(o_path, 'sources')
if not op.exists(o_path):
    os.mkdir(o_path)

o_path = op.join(o_path, subject)
if not op.exists(o_path):
    os.mkdir(o_path)

o_path = op.join(o_path, condition)
if not op.exists(o_path):
    os.mkdir(o_path)

fc.save(op.join(o_path, 'results-markers.hdf5'), overwrite=True)