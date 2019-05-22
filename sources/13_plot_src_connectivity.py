import os.path as op
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns

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

markers = ['plv_alpha', 'plv_theta', 'wpli_alpha', 'wpli_theta',
           'wsmi_alpha', 'wsmi_theta']
labels = {
    'PSD.delta': r'$\delta$',
    'PSD.theta': r'$\theta$',
    'PSD.alpha': r'$\alpha$',
    'PSD.beta': r'$\beta$',
    'PSD.gamma': r'$\gamma$',
    'wsmi_theta': r'wSMI $\theta$',
    'wsmi_alpha': r'wSMI $\alpha$',
    'wpli_theta': r'wPLI $\theta$',
    'wpli_alpha': r'wPLI $\alpha$',
    'plv_theta': r'PLV $\theta$',
    'plv_alpha': r'PLV $\alpha$',
    'Complexity': r'K',
    'MSF': r'MSF',
    'SE': r'SE',
}



groups = {
    'A+N+': ['A+N+'], 
    'A-N+': ['A-N+'], 
    'A+N-': ['A+N-'], 
    'A-N-': ['A-N-']}

contrasts = ['A-N-|A+N+', 'A-N-|A+N-', 'A-N-|A-N+']
# contrasts_titles = ['A+N+|A-N-', 'A+N-|A-N-', 'A-N+|A-N-']


# Read Data
df = pd.read_csv('data/all_values.csv', sep=';')
df_ec = df[df['condition'] == 'EC']

df_ec = df_ec.replace({'groupe': {'/': ''}}, regex=True)

df_ec['reg_a'] = [x.split('-')[0] for x in df_ec['regions'].values]
df_ec['reg_b'] = [x.split('-')[1] for x in df_ec['regions'].values]


for t_marker in markers:
    df_stats = None
    df_fdr_stats = None
    # Check if we have stats
    stats_fname = 'stats/contrast_{}.csv'.format(t_marker)
    if op.exists(stats_fname):
        df_stats = pd.read_csv(stats_fname, sep=';')
        regions = [x.split('.')[0] for x in df_stats['contrast'].values]
        reg_a = [x.split('-')[0] for x in regions]
        reg_b = [x.split('-')[1] for x in regions]
        df_stats['regions'] = regions
        df_stats['reg_a'] = reg_a
        df_stats['reg_b'] = reg_b

        contrast = [x.split('.')[-1].replace(
            'moins', '-').replace('plus', '+').replace('_', '|')
            for x in df_stats['contrast'].values]
        df_stats['group_contrast'] = contrast

    fdr_stats_fname = 'stats/contrast_{}_fdr.csv'.format(t_marker)
    if op.exists(fdr_stats_fname):
        df_fdr_stats = pd.read_csv(fdr_stats_fname, sep=';')
        regions = [x.split('.')[0] for x in df_fdr_stats['contrast'].values]
        reg_a = [x.split('-')[0] for x in regions]
        reg_b = [x.split('-')[1] for x in regions]
        df_fdr_stats['regions'] = regions
        df_fdr_stats['reg_a'] = reg_a
        df_fdr_stats['reg_b'] = reg_b

        contrast = [x.split('.')[-1].replace(
            'moins', '-').replace('plus', '+').replace('_', '|')
            for x in df_fdr_stats['contrast'].values]
        df_fdr_stats['group_contrast'] = contrast

    t_df = df_ec[['reg_a', 'reg_b', 'ID', 'marker', 'value', 'groupe']]
    t_df = t_df[t_df['marker'] == t_marker]

    t_df = t_df.groupby(['reg_a', 'reg_b', 'groupe']).mean().reset_index()
    mask = t_df['reg_a'] != t_df['reg_b']
    masked_df = t_df[mask]
    vmin = masked_df['value'].min()
    vmax = masked_df['value'].max()

    vmin = np.trunc(vmin * 1000) / 1000
    vmax = (np.trunc(vmax * 1000) + 1) / 1000 

    fig_groups, axes_groups = plt.subplots(
        int(len(groups) / 2), int(len(groups) / 2), dpi=70, figsize=(10, 10))

    axes_groups = axes_groups.ravel()

    group_name = 'A+N+'
    group_items = ['A+N+']

    for i_group, (group_name, group_items) in enumerate(groups.items()):
        t_ax = axes_groups[i_group]
        t_g_df = t_df[t_df['groupe'].isin(group_items)]

        tt = t_g_df.pivot('reg_b', 'reg_a', 'value')
        for x in tt.columns:
            tt.loc[x, x] = np.nan
        
        sns.heatmap(tt, cmap='viridis', square=True, ax=t_ax, 
                    vmin=vmin, vmax=vmax)
        t_ax.set_title(group_name, fontsize=14)
        t_ax.set_xlabel('')
        t_ax.set_ylabel('')
        t_ax.set_yticklabels(t_ax.get_yticklabels(), rotation=0)


    fig_groups.suptitle(labels[t_marker])
    fig_groups.savefig('figs/src_groups_{}.pdf'.format(t_marker))
    plt.close(fig_groups)

    if df_stats is not None:
        stat_vmin = np.log10(1)
        stat_m3 = -np.log10(1e-3)
        stat_m4 = -np.log10(1e-4)
        stat_vmax = -np.log10(1e-5)
        stat_logpsig = -np.log10(0.05)
        cmap = get_log_topomap(stat_logpsig, stat_vmin, stat_vmax)
        
        df_stats['logp'] = -np.log10(df_stats['p.value'])
        fig_contrasts, axes_contrasts = plt.subplots(
            int(np.ceil(len(contrasts) / 2)), 2, 
            dpi=70, figsize=(10, 10))
        axes_contrasts = axes_contrasts.ravel()
        
        for i_contrast, contrast in enumerate(contrasts):
            t_ax = axes_contrasts[i_contrast]
            t_c_df = df_stats[df_stats['group_contrast'] == contrast]

            tt = t_c_df.pivot('reg_b', 'reg_a', 'logp')
            for x in tt.columns:
                tt.loc[x, x] = np.nan
            
            sns.heatmap(tt, cmap=cmap, square=True, ax=t_ax, 
                        vmin=stat_vmin, vmax=stat_vmax)
            t_ax.set_title(contrast, fontsize=14)
            t_ax.set_xlabel('')
            t_ax.set_ylabel('')
            t_ax.set_yticklabels(t_ax.get_yticklabels(), rotation=0)
            cbar = t_ax.collections[0].colorbar
            cbar.set_ticks(
                [stat_vmin, stat_logpsig, stat_m3, stat_m4, stat_vmax])
            cbar.set_ticklabels([r"$p=1$",
                                r"$p=0.05$",
                                r"$p=1e^{-3}$",
                                r"$p=1e^{-4}$",
                                r"$p=1e^{-5}$"])
        if len(contrasts) % 2 != 0:
            axes_contrasts[-1].axis('off')

        fig_contrasts.suptitle(labels[t_marker])
        fig_contrasts.savefig('figs/src_contrast_{}.pdf'.format(t_marker))
        plt.close(fig_contrasts)

    if df_fdr_stats is not None:
        stat_vmin = np.log10(1)
        stat_m3 = -np.log10(1e-3)
        stat_m4 = -np.log10(1e-4)
        stat_vmax = -np.log10(1e-5)
        stat_logpsig = -np.log10(0.05)
        cmap = get_log_topomap(stat_logpsig, stat_vmin, stat_vmax)
        
        df_fdr_stats['logp'] = -np.log10(df_fdr_stats['p.value'])
        fig_contrasts, axes_contrasts = plt.subplots(
            int(np.ceil(len(contrasts) / 2)), 2, 
            dpi=70, figsize=(10, 10))
        axes_contrasts = axes_contrasts.ravel()
        
        for i_contrast, contrast in enumerate(contrasts):
            t_ax = axes_contrasts[i_contrast]
            t_c_df = df_fdr_stats[df_fdr_stats['group_contrast'] == contrast]

            tt = t_c_df.pivot('reg_b', 'reg_a', 'logp')
            for x in tt.columns:
                tt.loc[x, x] = np.nan
            
            sns.heatmap(tt, cmap=cmap, square=True, ax=t_ax, 
                        vmin=stat_vmin, vmax=stat_vmax)
            t_ax.set_title(contrast, fontsize=14)
            t_ax.set_xlabel('')
            t_ax.set_ylabel('')
            t_ax.set_yticklabels(t_ax.get_yticklabels(), rotation=0)
            cbar = t_ax.collections[0].colorbar
            cbar.set_ticks(
                [stat_vmin, stat_logpsig, stat_m3, stat_m4, stat_vmax])
            cbar.set_ticklabels([r"$p=1$",
                                r"$p=0.05$",
                                r"$p=1e^{-3}$",
                                r"$p=1e^{-4}$",
                                r"$p=1e^{-5}$"])
        if len(contrasts) % 2 != 0:
            axes_contrasts[-1].axis('off')

        fig_contrasts.suptitle('{} (FDR corrected)'.format(labels[t_marker]))
        fig_contrasts.savefig('figs/src_contrast_{}_fdr.pdf'.format(t_marker))
        plt.close(fig_contrasts)