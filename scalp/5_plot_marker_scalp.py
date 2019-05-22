import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns

from nice_ext.equipments import prepare_layout
from nice_ext.viz.topos import plot_topomap_multi_cbar
from nice_ext.viz.utils import get_log_topomap

# Configure plotting

sns.set_context('paper', rc={'font.size': 12, 'axes.labelsize': 12,
                             'xtick.labelsize': 10, 'ytick.labelsize': 10})
sns.set_style('white',
              {'font.sans-serif': ['Helvetica'], 'pdf.fonttype': 42,
               'axes.edgecolor': '.8'})
mpl.rcParams.update({'font.weight': '100'})
sns.set_color_codes()
current_palette = sns.color_palette()
mpl_palette = sns.color_palette(palette=None)

# Read markers data
df_electrodes = pd.read_csv(
    '../data/2019_01_17_nettoyages_metrics_electrodes.csv', sep=';')
df_metadata = df_electrodes[['id_MEMENTO', 'groupe']].drop_duplicates()
df_metadata = df_metadata.set_index('id_MEMENTO')  
electrodes = ['E{}'.format(i) for i in range(1, 225)]

scalp = np.arange(0, 224)
non_scalp = np.arange(224, 256)

layout, outlines = prepare_layout('egi/256')
pos = layout.pos[:, :2]
mask = np.in1d(np.arange(len(pos)), scalp)
mask_params = dict(marker='+', markerfacecolor='k', markeredgecolor='k',
                    linewidth=0, markersize=1)

# fig_type should be any of ['main', 'conn', 'n', 'a']

fig_type = 'n'

if fig_type == 'main':
    markers = [
        'PSD.delta', 'PSD.theta', 'PSD.alpha', 'PSD.beta', 'PSD.gamma',
        'MSF', 'SE', 'Complexity', 'wSMI.theta', 'wSMI.alpha']
elif fig_type == 'conn':
    markers = [
        'wSMI.theta', 'wSMI.alpha', 'wPLI.theta', 'wPLI.alpha', 
        'PLV.theta', 'PLV.alpha']
elif fig_type in ['n', 'a']:
    markers = [
        'PSD.delta', 'PSD.theta', 'PSD.alpha', 'PSD.beta', 'PSD.gamma',
        'MSF', 'SE', 'Complexity', 'wSMI.theta', 'wSMI.alpha',
        'wPLI.theta', 'wPLI.alpha', 'PLV.theta', 'PLV.alpha']

if fig_type in ['main', 'conn']:
    groups = {
        'A+N+': ['A+N+'], 
        'A-N+': ['A-N+'], 
        'A+N-': ['A+N-'], 
        'A-N-': ['A-N-']}

    contrasts = ['A+N+|A-N-', 'A-N+|A-N-', 'A+N-|A-N-']
elif fig_type == 'a':
    groups = {
        'A+': ['A+N+', 'A+N-'], 
        'A-': ['A-N+', 'A-N-']}

    contrasts = ['A+|A-']
elif fig_type == 'n':
    groups = {
        'N+': ['A+N+', 'A-N+'], 
        'N-': ['A+N-', 'A-N-']}

    contrasts = ['N+|N-']


if fig_type in ['main', 'conn']:
    figsize = (1.5 * (len(groups) + len(contrasts) + 2), 
               1.5 * len(markers))
    hspace = 0.1
    wspace = 0.1
    left = 0.05
elif fig_type in ['a', 'n']:
    figsize = (1.5 * (len(groups) + len(contrasts)), 
               1.5 * len(markers))
    hspace = 0.2
    wspace = 0.1
    left = 0.08

if fig_type == 'main':
    fig_out_fname = 'markers_scalp_topos'
elif fig_type == 'conn':
    fig_out_fname = 'sup_markers_scalp_topos'
elif fig_type == 'a':
    fig_out_fname = 'markers_scalp_topos_a'
elif fig_type == 'n':
    fig_out_fname = 'markers_scalp_topos_n'


units = {
    'PSD.delta': 'dB/Hz',
    'PSD.theta': 'dB/Hz',
    'PSD.alpha': 'dB/Hz',
    'PSD.beta': 'dB/Hz',
    'PSD.gamma': 'dB/Hz',
    'MSF': 'Hz',
    'SE': '',
    'Complexity': '',
    'wSMI.theta': '',
    'wSMI.alpha': '',
    'wPLI.theta': '',
    'wPLI.alpha': '',
    'PLV.theta': '',
    'PLV.alpha': ''
}

labels = {
    'PSD.delta': r'$\delta$',
    'PSD.theta': r'$\theta$',
    'PSD.alpha': r'$\alpha$',
    'PSD.beta': r'$\beta$',
    'PSD.gamma': r'$\gamma$',
    'wSMI.theta': r'wSMI $\theta$',
    'wSMI.alpha': r'wSMI $\alpha$',
    'wPLI.theta': r'wPLI $\theta$',
    'wPLI.alpha': r'wPLI $\alpha$',
    'PLV.theta': r'PLV $\theta$',
    'PLV.alpha': r'PLV $\alpha$',
    'Complexity': r'K',
    'MSF': r'MSF',
    'SE': r'SE',
}

fig, axes = plt.subplots(len(markers), len(groups) + len(contrasts) + 2,
                         figsize=figsize, dpi=70)

for i_marker, t_marker in enumerate(markers):

    t_df = df_electrodes[['id_MEMENTO', 'electrode', t_marker]]  
    t_df = t_df.pivot(index='id_MEMENTO', columns='electrode') 
    columns = [x[1] for x in t_df.columns]
    t_df.columns = columns
    t_df = t_df[electrodes]
    t_df = t_df.join(df_metadata) 

    group_means = np.zeros((len(groups), 256), dtype=np.float)
    for i_group, (t_title, t_group) in enumerate(groups.items()):
        t_vals = t_df[t_df['groupe'].isin(t_group)][electrodes].values.mean(0)
        group_means[i_group, scalp] = t_vals
        group_means[i_group, non_scalp] = np.min(t_vals)

    vmin = np.min(group_means)
    vmax = np.max(group_means)

    for i_group, (t_title, t_group) in enumerate(groups.items()):
        topo = group_means[i_group]
        ax = axes[i_marker, i_group]
        
        if i_group == 0:
            ax.set_ylabel(labels[t_marker], rotation=90, labelpad=4)

        title = t_title if i_marker == 0 else ''
        plot_topomap_multi_cbar(
            topo, pos, ax, title=title, cmap='viridis',
            outlines=outlines, mask=mask,
            mask_params=mask_params, sensors=False,
            vmin=vmin, vmax=vmax,
            colorbar=False)

        if i_group == len(groups) - 1:
            im = ax.images[0]
            divider = make_axes_locatable(axes[i_marker, i_group + 1])
            cax = divider.append_axes("left", size="5%", pad=0.05)
            cbar = plt.colorbar(im, cax=cax, 
                                ticks=(vmin, vmax),
                                format='%0.3f')
            axes[i_marker, i_group + 1].axis('off')
            cbar.set_label(units[t_marker])
            cbar.ax.get_yaxis().labelpad = -15
            cbar.ax.tick_params(labelsize=8)

    all_c_results = []
    for i_contrast, t_contrast in enumerate(contrasts):
        c_name = t_contrast.replace(
            '+', 'pos').replace('-', 'neg').replace('|', '_') 
        m_name =  t_marker.replace('.', '_')
        fname = '{}_{}.csv'.format(c_name, m_name)
        c_results = pd.read_csv('stats/{}'.format(fname), sep=';')
        c_results['contrast'] = t_contrast
        all_c_results.append(c_results[['electrode', 'p', 'contrast']])

    all_c_results = pd.concat(all_c_results)

    all_c_results = all_c_results.pivot(index='contrast', columns='electrode')
    columns = [x[1] for x in all_c_results.columns]
    all_c_results.columns = columns
    all_c_results = all_c_results[electrodes].reset_index()

    stat_vmin = np.log10(1)
    stat_vmax = -np.log10(1e-5)
    stat_logpsig = -np.log10(0.05)
    cmap = get_log_topomap(stat_logpsig, stat_vmin, stat_vmax)

    for i_contrast, t_contrast in enumerate(contrasts):
        ax = axes[i_marker, len(groups) + 1 + i_contrast]
        t_vals = all_c_results.query(
            "contrast == '{}'".format(t_contrast))[electrodes].values
        mask_stat = np.zeros(256, dtype=np.bool)
        mask_stat[scalp] = t_vals < 0.05
        topo = np.zeros(256, dtype=np.float)
        topo[scalp] = -np.log10(t_vals)
        title = t_contrast if i_marker == 0 else ''
        plot_topomap_multi_cbar(
            topo, pos, ax, title=title,
            cmap=cmap, outlines=outlines, mask=mask_stat,
            mask_params=mask_params, sensors=False,
            vmin=stat_vmin, vmax=stat_vmax, colorbar=False)
        
        if i_contrast == len(contrasts) - 1:
            im = ax.images[0]
            divider = make_axes_locatable(
                axes[i_marker, len(groups) + 2 + i_contrast])
            cax = divider.append_axes("left", size="5%", pad=0.05)
            cbar = plt.colorbar(im, cax=cax, ticks=(stat_vmin, stat_vmax),
                                format='%0.3f')
            cbar.ax.get_yaxis().labelpad = -15
            cbar.set_ticks([stat_vmin, stat_logpsig, stat_vmax])
            cbar.set_ticklabels(['p={}'.format(1), 
                                'p={}'.format(0.05),
                                'p={}'.format(1e-5)])
            cbar.ax.tick_params(labelsize=8)
            axes[i_marker, len(groups) + 2 + i_contrast].axis('off')

fig.subplots_adjust(
    top=0.95,
    bottom=0.01,
    left=left,
    right=0.9,
    hspace=hspace,
    wspace=wspace
)

fig.savefig('figs/{}.pdf'.format(fig_out_fname))