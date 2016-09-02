import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # improves plot aesthetics
import pandas as pd

table = pd.read_csv('teams_data_2016.csv', sep= ';', index_col = 0)

team_data = {}

for row in table.iterrows():
    index, data = row
    temp = []
    temp.append(data.tolist())
    team_data[index] = temp[0]

def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1) 
                     * (x2 - x1) + x1)
    return sdata

class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360./len(variables))

        axes = [fig.add_axes([0.1,0.1,0.8,0.8],polar=True,
                label = "axes{}".format(i)) 
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles, 
                                         labels=variables)
        [txt.set_rotation(angle-90) for txt, angle 
             in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], 
                               num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2)) 
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i])
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

# example data
variables = ("Efectividad Ofensiva", "Efectividad Defensiva", "Goles a Favor", "Goles en Contra", "Tiros al Arco a Favor", 
            "Tiros al Arco en Contra", 'Posesion de Pelota','Tarjetas Recibidas')

sl_data = team_data['SL']
nob_data = team_data['NOB']

ranges = [(12.0, 38.0), (41.0, 16.0), (0.5, 1.75),
         (1.88, 0.59), (3.0, 5.3), (6.1, 2.6), (42.0, 60.0), (3.2, 1.7)]            
# plotting
fig1 = plt.figure(figsize=(9, 9))
radar = ComplexRadar(fig1, variables, ranges)
radar.plot(sl_data)
radar.fill(sl_data,alpha=0.2)
radar.plot(nob_data,'0.15')
radar.fill(nob_data, '0.15', alpha=0.2)
plt.show()