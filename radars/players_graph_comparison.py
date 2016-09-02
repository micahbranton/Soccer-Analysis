import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # improves plot aesthetics
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--player1', '-p1', nargs='+', required=True,
                    help=('Jugador 1. Pasamelo con --player1 o -p1'))
parser.add_argument('--player1_plot', '-p1p', nargs='+', required=False,
                    help=('Color de Plot del Jugador 1. Pasamelo con --player1_plot o -p1p'))
parser.add_argument('--player1_fill', '-p1f', nargs='+', required=False,
                    help=('Color de Fill del Jugador 1. Pasamelo con --player1_fill o -p1f'))
parser.add_argument('--player2', '-p2', nargs='+', required=True,
                    help='Jugador 2. Pasamelo con --player2 o -p2')
parser.add_argument('--player2_plot', '-p2p', nargs='+', required=False,
                    help=('Color de Plot del Jugador 2. Pasamelo con --player1_plot o -p2p'))
parser.add_argument('--player2_fill', '-p2f', nargs='+', required=False,
                    help=('Color de Fill del Jugador 2. Pasamelo con --player1_fill o -p2f'))

args = parser.parse_args()

table = pd.read_csv('players_data_2016.csv', sep= ';', index_col = 0)

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
variables = ("Goles (Descontando Penales)", "Tiros Totales", "Precision de Tiros %",  "Dribles Correctos", 
            "Pases en Profundidad", "Centros", "Asistencias", "Pases Clave", "Pases Correctos %",
            "Tackles + Intercepciones", "Perdidas", "Duelos Aereos Ganados %", "Conversion de Goles %")

player1 = args.player1[0]
player2 = args.player2[0]

player1_data_raw = player_data[player1]
player1_data = []

for data in player1_data_raw:
    if data == 0:
        new_data = 0.001
    else:
        new_data = data
    player1_data.append(new_data)

player2_data_raw = player_data[player2]
player2_data = []

for data in player2_data_raw:
    if data == 0:
        new_data = 0.001
    else:
        new_data = data
    player2_data.append(new_data)

ranges = [(0.001, 0.85), (0.10, 4.40), (0.001, 80), (0.10, 4.60),
         (0.001, 0.40), (0.001, 3.2), (0.001, 0.45), (0.19, 3.05), (30, 95),
         (0.08, 8.40), (5.80, 0.39), (0.001, 70.00), (0.001, 100.00)]            
# plotting
fig1 = plt.figure(figsize=(9, 9))
radar = ComplexRadar(fig1, variables, ranges)
if args.player1_plot:
    player1_plot = args.player1_plot[0]
    radar.plot(player1_data, player1_plot)
else:
    radar.plot(player1_data)
if args.player1_fill:
    player1_fill = args.player1_fill[0]
    radar.fill(player1_data, player1_fill, alpha=0.2)
else:
    radar.fill(player1_data, alpha=0.2)
if args.player2_plot:
    player2_plot = args.player2_plot[0]
    radar.plot(player2_data, player2_plot)
else:
    radar.plot(player2_data)
if args.player2_fill:
    player2_fill = args.player2_fill[0]
    radar.fill(player2_data, player2_fill,alpha=0.2)
else:
    radar.fill(player2_data,alpha=0.2)

plt.show()
