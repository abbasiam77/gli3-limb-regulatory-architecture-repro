"""Reproduce Figure 4 from the audited S8 data export only.
Usage: python build_fig4_from_S8.py
Dependencies: numpy, matplotlib. The CSV is exported verbatim from ESM_2 S8.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

BASE = Path(__file__).resolve().parent
source=BASE.parent/'data'/'Fig4_TableS8_source.csv'
OUTPUT=BASE.parent/'outputs'/'reproduced'
OUTPUT.mkdir(parents=True, exist_ok=True)
with source.open(newline='', encoding='utf-8') as f:
    records=list(csv.DictReader(f))
assert len(records)==54, 'Expected 54 enhancer rows'
cols=['HOXA13','HOXD13','GLI3','H3K4me1','H3K27ac','H3K4me3','HAND2','p300','PITX1']
labels=[r['Enhancer ID'] for r in records]
classes=[r['Analysis class'] for r in records]
assert classes.count('limb')==13 and classes.count('non_limb')==41
values=np.array([[float(r[c]) for c in cols] for r in records], dtype=float)
assert np.isfinite(values).all() and (values>0).all() and (values<=1).all()
means=np.array([float(r['Mean rank percentile']) for r in records])
assert np.allclose(values.mean(axis=1),means,atol=1e-12)
assert np.all(np.diff(means)<=1e-12), 'Original ordering is not decreasing'
labels=[('CNE14_hs1586_mm1977' if s.startswith('CNE14/hs1586') else s) + (' (L)' if c=='limb' else ' (NL)') for s,c in zip(labels, classes)]

# Original portrait page dimensions: 511.2 x 676.8 pt (~7.1 x 9.4 in)
fig=plt.figure(figsize=(7.1,9.4), facecolor='white')
# Fixed layout, with an independent vector class strip, vector text and vector grid cells.
ax=fig.add_axes([0.216,0.112,0.647,0.865])
# pcolormesh produces 486 vector-filled cells, not a raster image.
x=np.arange(10)
y=np.arange(55)
ax.pcolormesh(x,y,values,cmap='viridis',vmin=0,vmax=1,shading='flat',rasterized=False,edgecolors='none')
ax.set_xlim(0,9); ax.set_ylim(54,0)
ax.set_yticks([])
for i,label in enumerate(labels):
    fig.text(.160, .112 + .865*(1-(i+.5)/54), label, ha='right', va='center', fontsize=5.5)
ax.set_xticks(np.arange(9)+.5,cols,rotation=55,ha='right',va='top',fontsize=8.0,rotation_mode='anchor')
ax.tick_params(axis='x',length=0,pad=5)
fig.text(.024,.545,'Enhancer',rotation=90,ha='center',va='center',fontsize=12)
ax.set_xlabel('Signal layer',fontsize=11,labelpad=11)
for spine in ax.spines.values(): spine.set_visible(True); spine.set_linewidth(.65)

# Class strip (blue=limb; orange=non-limb), aligned precisely to the heatmap rows.
strip=fig.add_axes([0.172,0.112,0.020,0.865]);strip.set_xlim(0,1);strip.set_ylim(54,0)
class_vals=np.array([1 if s=='limb' else 0 for s in classes])[:,None]
strip.pcolormesh([0,1],np.arange(55),class_vals,cmap=ListedColormap(['#f28e2b','#4e79a7']),vmin=0,vmax=1,shading='flat',rasterized=False)
strip.set_xticks([]);strip.set_yticks([])
for spine in strip.spines.values():spine.set_linewidth(.65)
fig.text(.182,.983,'Class',ha='center',va='bottom',fontsize=9)

# Color scale. The legend is deliberately independent of figure data values.
cax=fig.add_axes([.891,.378,.022,.28])
cb=fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(0,1),cmap='viridis'),cax=cax)
cb.set_ticks([0,.2,.4,.6,.8,1]);cb.ax.tick_params(labelsize=8,length=2)
cb.set_label('Within-layer rank percentile',fontsize=10,labelpad=8)

# Class legend placed underneath the data; not part of the 54x9 matrix.
from matplotlib.patches import Patch
fig.legend(handles=[Patch(facecolor='#f28e2b',edgecolor='none',label='Non-limb (NL)'),Patch(facecolor='#4e79a7',edgecolor='none',label='Limb (L)')],
           loc='lower left',bbox_to_anchor=(.018,.027),frameon=False,fontsize=7.3,ncol=1,
           handlelength=.85,handleheight=.85,handletextpad=.5,labelspacing=.16)
metadata={'Title':'Figure 4 — Within-layer rank percentiles from Supplementary Table S8',
          'Subject':'Reproducible vector heatmap generated directly from 54 x 9 Supplementary Table S8 numeric matrix',
          'Creator':'Matplotlib', 'Author':'Amir Ali Abbasi'}
fig.savefig(OUTPUT/'Fig4_S8_Vector_Final.pdf',format='pdf',metadata=metadata)
fig.savefig(OUTPUT/'Fig4_S8_Vector_Preview.png',format='png',dpi=220)
plt.close(fig)
print('Saved PDF and preview; data',values.shape,'min/max',values.min(),values.max())
