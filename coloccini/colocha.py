import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

table = pd.read_csv('colocha.csv', sep= ';', index_col = 0)

table['tackle_acc_%'] = table['tackle_acc']*100
season = table.index.values.tolist()
tackles = table['tackles'].tolist()
drib_past = table['drib_past'].tolist()
inter = table['inter'].tolist()
fouls = table['fouls'].tolist()
shots_block = table['shots_block'].tolist()
tackle_acc = table['tackle_acc_%'].tolist()
aerial_won = table['aerial_won'].tolist()
fouls_size = 700*table['fouls']
sizes = fouls_size.tolist()


fig, ax = plt.subplots()
ax.scatter(tackles, tackle_acc, s = 300, alpha=0.5, color=['b', 'b', 'b', 'r'])
ax.set_axis_bgcolor('0.97')

for i, txt in enumerate(season):
	ax.annotate(txt, xy=(tackles[i], tackle_acc[i]), xytext=(tackles[i], tackle_acc[i]+1), size = 13)

plt.title('Quites', fontsize = 20, weight = 'bold')
plt.xlabel('Quites Totales por 90 Minutos', fontsize = 13)
plt.ylabel('Efectividad en Quites (%)', fontsize = 13)

plt.show()

# x = np.array([0,1,2,3])
# plt.xticks(x, season)
# plt.plot(x, aerial_won, marker='o')
# plt.legend()
# plt.show()

# fig, ax = plt.subplots()
# ax.scatter(inter, shots_block, s = sizes, alpha=0.5, color=['b', 'b', 'b', 'r'])
# ax.set_axis_bgcolor('0.97')

# for i, txt in enumerate(season):
# 	ax.annotate(txt, xy=(inter[i], shots_block[i]), xytext=(inter[i], shots_block[i]+0.03), size = 13)
# ax.annotate('El tamaño indica cantidad de faltas cometidas por 90 minutos', xy=(2.05, 0.86), size = 9, color='0.12', style='italic')


# plt.title('Intercepciones vs Tiros Bloqueados', fontsize = 20, weight = 'bold')
# plt.xlabel('Intercepciones por 90 Minutos', fontsize = 13)
# plt.ylabel('Tiros Bloqueados por 90 Minutos', fontsize = 13)

# plt.show()