import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc
import numpy as np
rc('font', **{'family': 'serif', 'serif': ['CMU Serif']})
# rc('text', usetex=True)
# rc('text.latex', preamble= r'\usepackage{amsfonts}')

data = pd.read_csv(r"D:\CSIRO_C3\ShotgunII_final\PlotC3Setups\data.csv")

fig, ax1 = plt.subplots()
plt.subplots_adjust(bottom=0.41,top=0.95,left=0.08)

N = len(data)

lns1 = ax1.vlines(np.arange(N), 0, data["Success"], linewidth=2, colors="tab:blue", label="Success Rate", zorder=2)
ax1.set_ylabel("Success Rate (%)")
ax1.set_xticks(np.arange(N))
ax1.set_xticklabels(data["Screen Name"], rotation=90)

ax2 = ax1.twinx()

lns2 = ax2.vlines(np.arange(N), 0, data["Setups"], linewidth=5, colors="tab:orange", label="#Setups", zorder=1)
ax2.set_ylabel("#Setups")

lns = [lns1,lns2]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# plt.plot(data["Success"]*100)
# plt.plot(data["Setups"])
ax1.set_zorder(ax2.get_zorder()+1)
ax1.patch.set_visible(False)

plt.savefig(r"D:\CSIRO_C3\ShotgunII_final\generated\C3Setups.pdf", dpi=90)
plt.show()