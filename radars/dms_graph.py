import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # improves plot aesthetics
import pandas as pd

table = pd.read_csv('dms.csv', sep= ';', index_col = 0)

player_data = {}

for row in table.iterrows():
    index, data = row
    temp = []
    temp.append(data.tolist())
    player_data[index] = temp[0]

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
        angles = np.arange(90, 450, 360./len(variables))

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
            gridlabel[1] = ""
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
variables = ("Goles (Descontando Penales)", "Dribles Correctos", "Pases en Profundidad",  "Asistencias", 
            "Pases Clave", "Pases Largos", "Pases Correctos %", "Intercepciones", "Quites",
             "Perdidas", "Duelos Aereos Ganados %", "Dribles pasados", "Fouls")


player1_data_raw = player_data['Pochettino']
player1_data = []

for data in player1_data_raw:
    if data == 0:
        new_data = 0.001
    else:
        new_data = data
    player1_data.append(new_data)

ranges = [(0.001, 0.85), (0.12, 4.60), (0.001, 0.40), (0.001, 0.36),
         (0.19, 3.05), (0.01, 6.5), (30, 90), (0.1, 5.30), (0.1, 5.5),
         (5.80, 0.39), (0.001, 70.00), (4.9, 0.1), (4.9, 0.1)]

# plotting
fig1 = plt.figure(figsize=(9, 9))
radar = ComplexRadar(fig1, variables, ranges)
radar.plot(player1_data, 'g')
radar.fill(player1_data, 'yellow',alpha=0.2)
plt.show()
