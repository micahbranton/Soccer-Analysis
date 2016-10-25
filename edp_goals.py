# =============================================================================
#          File: edp_goals.py
#        Author: Andre Brener
#       Created: 24 Oct 2016
# Last Modified: 24 Oct 2016
#   Description: description
# =============================================================================
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

title = 'Goles de Estudiantes en el Campeonato'
plt.figure(figsize=(8, 8))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
plt.style.use('fivethirtyeight')
plt.title(title, weight='bold', loc='left', fontsize=22)
labels = 'Jugada', 'Pelota Parada', 'Penal'
sizes = [6, 7, 1]
colors = ['limegreen', 'deepskyblue', 'orangered']
ax.text(0.2, 1.16, 'Goles a favor por 90 minutos jugados',
        color='0.3', fontsize=16, horizontalalignment='right')
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', labeldistance=1.05, startangle=90)
# for n, val in enumerate(y):
# value = round(val, 2)
# ax.annotate(value,
# xy=(x[n],
# val),
# xytext=(x[n],
# val),
# verticalalignment='bottom',
# horizontalalignment='center',
# color='0.3',
# fontsize=18)


plt.show()

# fig.savefig('/Users/andre/Desktop/blandi.png')
