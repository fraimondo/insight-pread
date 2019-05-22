import os
import os.path as op
from glob import glob

from scipy import io as sio

import time
import mne
from mne.utils import logger

from argparse import ArgumentParser
import sys
import traceback

sys.path.append('../')
from common import get_scalp_markers, get_scalp_reductions


start_time = time.time()

parser = ArgumentParser(
    description='Compute markers on selected EEG file')

parser.add_argument('--subject', metavar='subject', nargs=1, type=str,
                    help='Subject name', required=True)

parser.add_argument('--path', metavar='db_path', nargs=1, type=str,
                    help='Database path', required=True)

args = parser.parse_args()
subject = args.subject
db_path = args.path

if isinstance(subject, list):
    subject = subject[0]

if isinstance(db_path, list):
    db_path = db_path[0]

if not op.exists(op.join(db_path, 'results')):
    os.mkdir(op.join(db_path, 'results'))


s_path = op.join(db_path, 'subjects', subject)

for condition in ['EC', 'EO']:
    results_dir = op.join(db_path, 'results', condition)
    if not op.exists(results_dir):
        os.mkdir(results_dir)

    if not op.exists(op.join(results_dir, subject)):
        os.mkdir(op.join(results_dir, subject))

    now = time.strftime('%Y_%m_%d_%H_%M_%S')
    log_suffix = '_{}.log'.format(now)
    mne.utils.set_log_file(op.join(results_dir, subject, subject + log_suffix))

    logger.info('Running {}'.format(subject))
    report = None
    try:
        # Read
        fnames = [x for x in glob(
            op.join(s_path, '*aramis-insight-egi-epo.fif'))]
        epochs = mne.read_epochs(fnames[0], preload=True, verbose=True)

        epochs = epochs[condition]
        
        # Fit
        fc = get_scalp_markers()
        fc.fit(epochs)
        out_fname = '{}_{}-markers.hdf5'.format(subject, now)

        # Save markers
        fc.save(op.join(results_dir, subject, out_fname), overwrite=True)

        # Summarize
        reductions = get_scalp_reductions()

        topos = fc.reduce_to_topo(reductions)
        out_fname = op.join(results_dir, subject, 'topos.mat')
        topo_names = fc.topo_names()
        to_save = {'names': topo_names, 'topos': topos}
        sio.savemat(out_fname, to_save)
    
    except Exception:
        msg = traceback.format_exc()
        logger.info(msg + '\nRunning subject failed ("%s")' % subject)
        sys.exit(-4)
    finally:
        elapsed_time = time.time() - start_time
        logger.info('Elapsed time {}'.format(
            time.strftime('%H:%M:%S', time.gmtime(elapsed_time))))
        logger.info('Running pipeline done')
