import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

file = 'player_in_goals_2016_9_26.csv'
table = pd.read_csv(file)


def blandi(string):
    if 'Blandi' in string:
        return 1


table['blandi'] = table['player'].apply(blandi)


blandi_table = table[table['blandi'] == 1][
    ['player', '90m_player_goals', '90m_team_goals']].T


blandi_table.head()


title = 'Goles de San Lorenzo en 2016'
fig, ax = plt.subplots(figsize=(7, 5))
ttl = ax.title
ttl.set_position([10, 1.05])
plt.style.use('fivethirtyeight')
plt.title(title, weight='bold', loc='left', fontsize=22)
x = np.arange(1, 3)
y = blandi_table[629][1:]
plt.bar(x, y, align='center', color="deepskyblue")
x_labels = ['Con Blandi en cancha', 'Sin Blandi en cancha']
plt.xticks(x, x_labels, color='0.3', fontsize=16)
plt.ylim(0, 2.2)
ax.set_yticklabels([])
ax.text(1.2, 2.05, 'Goles a favor por 90 minutos jugados',
        color='0.3', fontsize=16, horizontalalignment='center')
for n, val in enumerate(y):
    value = round(val, 2)
    ax.annotate(value,
                xy=(x[n],
                    val),
                xytext=(x[n],
                        val),
                verticalalignment='bottom',
                horizontalalignment='center',
                color='0.3',
                fontsize=18)


plt.show()

fig.savefig('/Users/andre/Desktop/blandi.png')
