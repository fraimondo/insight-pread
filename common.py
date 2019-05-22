from nice import Markers
from nice.markers import (PowerSpectralDensity,
                          KolmogorovComplexity,
                          PermutationEntropy,
                          SymbolicMutualInformation,
                          PowerSpectralDensitySummary,
                          PowerSpectralDensityEstimator)

from nice_sandbox.markers.connectivity import (WeightedPhaseLagIndex,
                                               PhaseLockingValue)


def get_scalp_markers():
        psds_params = dict(n_fft=4096, n_overlap=100, n_jobs='auto', nperseg=128)

    base_psd = PowerSpectralDensityEstimator(
        psd_method='welch', tmin=None, tmax=1.0, fmin=1., fmax=45.,
        psd_params=psds_params, comment='default')

    f_list = [
        PowerSpectralDensity(estimator=base_psd, fmin=1., fmax=4.,
                             normalize=False, comment='delta'),
        PowerSpectralDensity(estimator=base_psd, fmin=1., fmax=4.,
                             normalize=True, comment='deltan'),
        PowerSpectralDensity(estimator=base_psd, fmin=4., fmax=8.,
                             normalize=False, comment='theta'),
        PowerSpectralDensity(estimator=base_psd, fmin=4., fmax=8.,
                             normalize=True, comment='thetan'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=12.,
                             normalize=False, comment='alpha'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=12.,
                             normalize=True, comment='alphan'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=10.,
                             normalize=False, comment='lowalpha'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=10.,
                             normalize=True, comment='lowalphan'),
        PowerSpectralDensity(estimator=base_psd, fmin=10., fmax=12.,
                             normalize=False, comment='highalpha'),
        PowerSpectralDensity(estimator=base_psd, fmin=10., fmax=12.,
                             normalize=True, comment='highalphan'),
        PowerSpectralDensity(estimator=base_psd, fmin=12., fmax=30.,
                             normalize=False, comment='beta'),
        PowerSpectralDensity(estimator=base_psd, fmin=12., fmax=30.,
                             normalize=True, comment='betan'),
        PowerSpectralDensity(estimator=base_psd, fmin=30., fmax=45.,
                             normalize=False, comment='gamma'),
        PowerSpectralDensity(estimator=base_psd, fmin=30., fmax=45.,
                             normalize=True, comment='gamman'),

        PowerSpectralDensity(estimator=base_psd, fmin=1., fmax=45.,
                             normalize=True, comment='summary_se'),
        PowerSpectralDensitySummary(estimator=base_psd, fmin=1., fmax=45.,
                                    percentile=.5, comment='summary_msf'),
        PowerSpectralDensitySummary(estimator=base_psd, fmin=1., fmax=45.,
                                    percentile=.9, comment='summary_sef90'),
        PowerSpectralDensitySummary(estimator=base_psd, fmin=1., fmax=45.,
                                    percentile=.95, comment='summary_sef95'),

        PermutationEntropy(tmin=None, tmax=1.0, backend='c', tau=8,
                           comment='theta',
                           method_params={'filter_freq': 8.0}),

        PermutationEntropy(tmin=None, tmax=1.0, backend='c', tau=4,
                           comment='alpha',
                           method_params={'filter_freq': 12.0}),

        # WSMI Theta (250/3/8 ~ <10.41 Hz)
        SymbolicMutualInformation(
            tmin=None, tmax=1.0, method='weighted', backend='openmp', tau=8,
            method_params={'nthreads': 'auto', 'bypass_csd': False,
                           'filter_freq': 8.0},
            comment='theta_weighted'),

        # WSMI Alpha (250/3/4 ~ <20.83 Hz)
        SymbolicMutualInformation(
            tmin=None, tmax=1.0, method='weighted', backend='openmp', tau=4,
            method_params={'nthreads': 'auto', 'bypass_csd': False,
                           'filter_freq': 12.0},
            comment='alpha_weighted'),

        # WSMI Beta (250/3/4 ~ <41.66 Hz)
        SymbolicMutualInformation(
            tmin=None, tmax=1.0, method='weighted', backend='openmp', tau=2,
            method_params={'nthreads': 'auto', 'bypass_csd': False,
                           'filter_freq': 30.0},
            comment='beta_weighted'),

        # WSMI Gamma (250/3/4 ~ <83.33 Hz)
        SymbolicMutualInformation(
            tmin=None, tmax=1.0, method='weighted', backend='openmp', tau=1,
            method_params={'nthreads': 'auto', 'bypass_csd': False,
                           'filter_freq': 45.0},
            comment='gamma_weighted'),

        WeightedPhaseLagIndex(tmin=None, tmax=1.0, fmin=0, fmax=8.0, 
                              comment='theta_weighted'),
        WeightedPhaseLagIndex(tmin=None, tmax=1.0, fmin=8.0, fmax=12.0, 
                              comment='alpha_weighted'),
        PhaseLockingValue(tmin=None, tmax=1.0, fmin=0, fmax=8.0, 
                          comment='theta'),
        PhaseLockingValue(tmin=None, tmax=1.0, fmin=8.0, fmax=12.0, 
                          comment='alpha'),

        KolmogorovComplexity(tmin=None, tmax=1.0, backend='openmp',
                             method_params={'nthreads': 'auto'}),
    ]

    fc = Markers(f_list)
    return fc


def get_src_markers():
        psds_params = dict(n_fft=4096, n_overlap=100, n_jobs='auto', nperseg=128)

    base_psd = PowerSpectralDensityEstimator(
        psd_method='welch', tmin=None, tmax=1.0, fmin=1., fmax=45.,
        psd_params=psds_params, comment='default')

    f_list = [
        PowerSpectralDensity(estimator=base_psd, fmin=1., fmax=4.,
                             normalize=False, comment='delta'),
        PowerSpectralDensity(estimator=base_psd, fmin=1., fmax=4.,
                             normalize=True, comment='deltan'),
        PowerSpectralDensity(estimator=base_psd, fmin=4., fmax=8.,
                             normalize=False, comment='theta'),
        PowerSpectralDensity(estimator=base_psd, fmin=4., fmax=8.,
                             normalize=True, comment='thetan'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=12.,
                             normalize=False, comment='alpha'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=12.,
                             normalize=True, comment='alphan'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=10.,
                             normalize=False, comment='lowalpha'),
        PowerSpectralDensity(estimator=base_psd, fmin=8., fmax=10.,
                             normalize=True, comment='lowalphan'),
        PowerSpectralDensity(estimator=base_psd, fmin=10., fmax=12.,
                             normalize=False, comment='highalpha'),
        PowerSpectralDensity(estimator=base_psd, fmin=10., fmax=12.,
                             normalize=True, comment='highalphan'),
        PowerSpectralDensity(estimator=base_psd, fmin=12., fmax=30.,
                             normalize=False, comment='beta'),
        PowerSpectralDensity(estimator=base_psd, fmin=12., fmax=30.,
                             normalize=True, comment='betan'),
        PowerSpectralDensity(estimator=base_psd, fmin=30., fmax=45.,
                             normalize=False, comment='gamma'),
        PowerSpectralDensity(estimator=base_psd, fmin=30., fmax=45.,
                             normalize=True, comment='gamman'),

        PowerSpectralDensity(estimator=base_psd, fmin=1., fmax=45.,
                             normalize=True, comment='summary_se'),
        PowerSpectralDensitySummary(estimator=base_psd, fmin=1., fmax=45.,
                                    percentile=.5, comment='summary_msf'),
        PowerSpectralDensitySummary(estimator=base_psd, fmin=1., fmax=45.,
                                    percentile=.9, comment='summary_sef90'),
        PowerSpectralDensitySummary(estimator=base_psd, fmin=1., fmax=45.,
                                    percentile=.95, comment='summary_sef95'),

        PermutationEntropy(tmin=None, tmax=1.0, backend='c', tau=8,
                           comment='theta',
                           method_params={'filter_freq': 8.0}),

        PermutationEntropy(tmin=None, tmax=1.0, backend='c', tau=4,
                           comment='alpha',
                           method_params={'filter_freq': 12.0}),

        # WSMI Theta (250/3/8 ~ <10.41 Hz)
        SymbolicMutualInformation(
            tmin=None, tmax=1.0, method='weighted', backend='openmp', tau=8,
            method_params={'nthreads': 'auto', 'bypass_csd': True,
                           'filter_freq': 8.0},
            comment='theta_weighted'),

        # WSMI Alpha (250/3/4 ~ <20.83 Hz)
        SymbolicMutualInformation(
            tmin=None, tmax=1.0, method='weighted', backend='openmp', tau=4,
            method_params={'nthreads': 'auto', 'bypass_csd': True,
                           'filter_freq': 12.0},
            comment='alpha_weighted'),

        WeightedPhaseLagIndex(tmin=None, tmax=1.0, fmin=0, fmax=8.0, 
                              comment='theta_weighted'),
        WeightedPhaseLagIndex(tmin=None, tmax=1.0, fmin=8.0, fmax=12.0, 
                              comment='alpha_weighted'),
        
        PhaseLockingValue(tmin=None, tmax=1.0, fmin=0, fmax=8.0, 
                          comment='theta'),
        PhaseLockingValue(tmin=None, tmax=1.0, fmin=8.0, fmax=12.0, 
                          comment='alpha'),

        KolmogorovComplexity(tmin=None, tmax=1.0, backend='openmp',
                             method_params={'nthreads': 'auto'}),
    ]

    fc = Markers(f_list)
    return fc


def trim_mean80(a, axis=0):
    return trim_mean(a, proportiontocut=.1, axis=axis)


def get_scalp_reductions():
    reduction_params = {}
    scalp_roi = np.arange(224)
    epochs_fun = trim_mean80
    channels_fun = np.mean

    reduction_params['PowerSpectralDensity'] = {
        'reduction_func':
            [{'axis': 'frequency', 'function': np.sum},
             {'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': scalp_roi}}

    reduction_params['PowerSpectralDensity/summary_se'] = {
        'reduction_func':
            [{'axis': 'frequency', 'function': entropy},
             {'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': scalp_roi}}

    reduction_params['PowerSpectralDensitySummary'] = {
        'reduction_func':
            [{'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': scalp_roi}}

    reduction_params['PermutationEntropy'] = {
        'reduction_func':
            [{'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': scalp_roi}}

    reduction_params['SymbolicMutualInformation'] = {
        'reduction_func':
            [{'axis': 'channels_y', 'function': np.median},
             {'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels_y': scalp_roi,
            'channels': scalp_roi}}

    reduction_params['KolmogorovComplexity'] = {
        'reduction_func':
            [{'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': scalp_roi}}

    reduction_params['WeightedPhaseLagIndex'] = {
        'reduction_func':
            [{'axis': 'channels_y', 'function': np.median},
             {'axis': 'channels', 'function': channels_fun}],
        'picks': {
            'channels_y': None,
            'channels': None}}

    reduction_params['PhaseLockingValue'] = {
        'reduction_func':
            [{'axis': 'channels_y', 'function': np.median},
             {'axis': 'channels', 'function': channels_fun}],
        'picks': {
            'channels_y': None,
            'channels': None}}

    return reduction_params


def get_src_reductions(config, config_params):
    reduction_params = {}
    scalp_roi = np.arange(224)
    epochs_fun = trim_mean80
    channels_fun = np.mean

    reduction_params['PowerSpectralDensity'] = {
        'reduction_func':
            [{'axis': 'frequency', 'function': np.sum},
             {'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': None}}

    reduction_params['PowerSpectralDensity/summary_se'] = {
        'reduction_func':
            [{'axis': 'frequency', 'function': entropy},
             {'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': None}}

    reduction_params['PowerSpectralDensitySummary'] = {
        'reduction_func':
            [{'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': None}}

    reduction_params['PermutationEntropy'] = {
        'reduction_func':
            [{'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': None}}

    reduction_params['SymbolicMutualInformation'] = {
        'reduction_func':
            [{'axis': 'channels_y', 'function': np.median},
             {'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels_y': None,
            'channels': None}}
    
    reduction_params['WeightedPhaseLagIndex'] = {
        'reduction_func':
            [{'axis': 'channels_y', 'function': np.median},
             {'axis': 'channels', 'function': channels_fun}],
        'picks': {
            'channels_y': None,
            'channels': None}}

    reduction_params['PhaseLockingValue'] = {
        'reduction_func':
            [{'axis': 'channels_y', 'function': np.median},
             {'axis': 'channels', 'function': channels_fun}],
        'picks': {
            'channels_y': None,
            'channels': None}}

    reduction_params['KolmogorovComplexity'] = {
        'reduction_func':
            [{'axis': 'channels', 'function': channels_fun},
             {'axis': 'epochs', 'function': epochs_fun}],
        'picks': {
            'epochs': None,
            'channels': None}}

    return reduction_params



_egi256_egi128_map = {
    'E1': 'E1', 'E100': 'E61', 'E101': 'E62', 'E103': 'E63', 'E105': 'E64',
    'E107': 'E65', 'E108': 'E66', 'E110': 'E67', 'E116': 'E70', 'E118': 'E71',
    'E119': 'E72', 'E121': 'E68', 'E122': 'E69', 'E125': 'E75', 'E127': 'E76',
    'E128': 'E77', 'E129': 'E78', 'E131': 'E79', 'E132': 'E80', 'E134': 'E73',
    'E136': 'E74', 'E141': 'E85', 'E143': 'E86', 'E144': 'E87', 'E147': 'E81',
    'E148': 'E82', 'E15': 'E11', 'E150': 'E83', 'E151': 'E84', 'E152': 'E91',
    'E153': 'E92', 'E160': 'E90', 'E162': 'E97', 'E163': 'E98', 'E164': 'E93',
    'E166': 'E88', 'E167': 'E89', 'E17': 'E13', 'E170': 'E96', 'E175': 'E94',
    'E177': 'E95', 'E179': 'E101', 'E18': 'E8', 'E181': 'E102', 'E182': 'E103',
    'E184': 'E104', 'E185': 'E105', 'E186': 'E106', 'E19': 'E9',
    'E190': 'E100', 'E192': 'E108', 'E194': 'E109', 'E195': 'E110',
    'E197': 'E111', 'E198': 'E112', 'E2': 'E2', 'E20': 'E10', 'E200': 'E99',
    'E202': 'E115', 'E204': 'E116', 'E209': 'E107', 'E21': 'E16',
    'E214': 'E117', 'E215': 'E118', 'E218': 'E113', 'E219': 'E114',
    'E220': 'E121', 'E221': 'E122', 'E223': 'E123', 'E224': 'E124',
    'E226': 'E125', 'E227': 'E120', 'E228': 'E119', 'E23': 'E12',
    'E238': 'E126', 'E241': 'E127', 'E25': 'E14', 'E252': 'E128',
    'E254': 'E43', 'E255': 'E48', 'E26': 'E15', 'E27': 'E18', 'E29': 'E19',
    'E30': 'E20', 'E31': 'E17', 'E32': 'E21', 'E33': 'E22', 'E35': 'E23',
    'E36': 'E24', 'E37': 'E25', 'E4': 'E3', 'E40': 'E27', 'E41': 'E28',
    'E43': 'E29', 'E44': 'E30', 'E45': 'E31', 'E47': 'E26', 'E5': 'E4',
    'E52': 'E36', 'E53': 'E37', 'E54': 'E32', 'E55': 'E33', 'E57': 'E34',
    'E58': 'E35', 'E6': 'E5', 'E61': 'E38', 'E64': 'E40', 'E65': 'E41',
    'E66': 'E42', 'E67': 'E44', 'E69': 'E39', 'E71': 'E46', 'E73': 'E49',
    'E74': 'E45', 'E77': 'E47', 'E79': 'E53', 'E8': 'E6', 'E80': 'E54',
    'E81': 'E55', 'E84': 'E50', 'E86': 'E51', 'E87': 'E52', 'E9': 'E7',
    'E92': 'E56', 'E94': 'E57', 'E96': 'E58', 'E98': 'E59', 'E99': 'E60'}


_egi256_egi64a_map = {
    'E2': 'E1', 'E5': 'E2', 'E8': 'E3', 'E10': 'E4', 'E12': 'E5', 'E15': 'E6',
    'E18': 'E7', 'E20': 'E8', 'E21': 'E9', 'E24': 'E10', 'E26': 'E11',
    'E27': 'E12', 'E29': 'E13', 'E34': 'E14', 'E36': 'E15', 'E37': 'E16',
    'E42': 'E17', 'E44': 'E18', 'E46': 'E19', 'E47': 'E20', 'E48': 'E21',
    'E49': 'E22', 'E59': 'E23', 'E62': 'E24', 'E64': 'E25', 'E66': 'E26',
    'E68': 'E27', 'E69': 'E28', 'E76': 'E29', 'E79': 'E30', 'E81': 'E31',
    'E84': 'E32', 'E86': 'E33', 'E87': 'E34', 'E88': 'E35', 'E96': 'E36',
    'E97': 'E37', 'E101': 'E38', 'E109': 'E39', 'E116': 'E40', 'E119': 'E41',
    'E126': 'E42', 'E140': 'E43', 'E142': 'E44', 'E143': 'E45', 'E150': 'E46',
    'E153': 'E47', 'E161': 'E48', 'E162': 'E49', 'E164': 'E50', 'E170': 'E51',
    'E172': 'E52', 'E179': 'E53', 'E183': 'E54', 'E185': 'E55', 'E194': 'E56',
    'E202': 'E57', 'E206': 'E58', 'E207': 'E59', 'E210': 'E60', 'E211': 'E61',
    'E213': 'E62', 'E222': 'E63', 'E224': 'E64'}


_egi256_egi32a_map = {
    'E37': 'E1', 'E18': 'E2', 'E34': 'E3', 'E12': 'E4', 'E47': 'E5',
    'E36': 'E6', 'E21': 'E7', 'E224': 'E8', 'E2': 'E9', 'E49': 'E10',
    'E24': 'E11', 'E207': 'E12', 'E213': 'E13', 'E69': 'E14', 'E59': 'E15',
    'E81': 'E16', 'E183': 'E17', 'E202': 'E18', 'E76': 'E19', 'E79': 'E20',
    'E143': 'E21', 'E172': 'E22', 'E96': 'E23', 'E87': 'E24', 'E101': 'E25',
    'E153': 'E26', 'E170': 'E27', 'E109': 'E28', 'E116': 'E29', 'E126': 'E30',
    'E150': 'E31', 'E140': 'E32'}

_egi256_egi16a_map = {
    'E37': 'E1', 'E18': 'E2', 'E47': 'E3', 'E2': 'E4', 'E36': 'E5',
    'E224': 'E6', 'E59': 'E7', 'E183': 'E8', 'E69': 'E9', 'E202': 'E10',
    'E87': 'E11', 'E153': 'E12', 'E96': 'E13', 'E170': 'E14', 'E116': 'E15',
    'E150': 'E16'}


_montage_map = {}
_montage_map['egi/128'] = _egi256_egi128_map
_montage_map['egi/64a'] = _egi256_egi64a_map
_montage_map['egi/32a'] = _egi256_egi32a_map
_montage_map['egi/16a'] = _egi256_egi16a_map


def map_montage(inst, dst):
    logger.info('Mapping montage to {}'.format(src, dst))
    rename = _montage_map[dst]
    to_keep = list(rename.keys())
    translated = inst.copy().pick_channels(to_keep)
    translated.rename_channels(rename)
    translated.info['description'] = dst
    return translated.pick_channels(get_ch_names(dst))



sources_labels = [
    'lh.bankssts',
    'lh.caudalanteriorcingulate',
    'lh.caudalmiddlefrontal',
    'lh.cuneus',
    'lh.entorhinal',
    'lh.frontalpole',
    'lh.fusiform',
    'lh.inferiorparietal',
    'lh.inferiortemporal',
    'lh.insula',
    'lh.isthmuscingulate',
    'lh.lateraloccipital',
    'lh.lateralorbitofrontal',
    'lh.lingual',
    'lh.medialorbitofrontal',
    'lh.middletemporal',
    'lh.paracentral',
    'lh.parahippocampal',
    'lh.parsopercularis',
    'lh.parsorbitalis',
    'lh.parstriangularis',
    'lh.pericalcarine',
    'lh.postcentral',
    'lh.posteriorcingulate',
    'lh.precentral',
    'lh.precuneus',
    'lh.rostralanteriorcingulate',
    'lh.rostralmiddlefrontal',
    'lh.superiorfrontal',
    'lh.superiorparietal',
    'lh.superiortemporal',
    'lh.supramarginal',
    'lh.temporalpole',
    'lh.transversetemporal',
    'rh.bankssts',
    'rh.caudalanteriorcingulate',
    'rh.caudalmiddlefrontal',
    'rh.cuneus',
    'rh.entorhinal',
    'rh.frontalpole',
    'rh.fusiform',
    'rh.inferiorparietal',
    'rh.inferiortemporal',
    'rh.insula',
    'rh.isthmuscingulate',
    'rh.lateraloccipital',
    'rh.lateralorbitofrontal',
    'rh.lingual',
    'rh.medialorbitofrontal',
    'rh.middletemporal',
    'rh.paracentral',
    'rh.parahippocampal',
    'rh.parsopercularis',
    'rh.parsorbitalis',
    'rh.parstriangularis',
    'rh.pericalcarine',
    'rh.postcentral',
    'rh.posteriorcingulate',
    'rh.precentral',
    'rh.precuneus',
    'rh.rostralanteriorcingulate',
    'rh.rostralmiddlefrontal',
    'rh.superiorfrontal',
    'rh.superiorparietal',
    'rh.superiortemporal',
    'rh.supramarginal',
    'rh.temporalpole',
    'rh.transversetemporal'
]