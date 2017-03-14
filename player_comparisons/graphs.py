# =============================================================================
#          File: graphs.py
#        Author: Andre Brener
#       Created: 31 Jan 2017
# Last Modified: 11 Feb 2017
#   Description: description
# =============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('river_data.csv')

players_in_graph = 7
chosen_player = 'Bergessio'
team = 'River'

stats_dict = {
    'total_shots': [
        'es el más tirador del equipo',
        'Top {0} de jugadores de {1} con más tiros por 90 minutos'.format(
            players_in_graph,
            team),
        1],
    'sot': [
        'fue el que más tiró al arco del equipo',
        'Top {0} de jugadores  de {1} con más tiros al arco por 90 minutos'.format(
            players_in_graph,
            team),
        1],
    'goals': [
        'fue el más goleador del equipo en el Torneo',
        'Top {0} de jugadores de {1} con más goles por 90 minutos'.format(
            players_in_graph,
            team),
        1],
    'key_passes': [
        'fue el que hizo más pases que terminaron en tiro',
        'Top {0} de jugadores de {1} que hicieron más pases que terminaron  en tiro por 90 minutos'.format(
            players_in_graph,
            team),
        1],
    'assists': [
        'fue el mejor asistidor de {0} en el Torneo'.format(team),
        'Top {0} de jugadores de {1} con más asistencias por 90 minutos'.format(
            players_in_graph,
            team),
        1]}


for col in df.columns:
    if col != 'player':
        # print('\n{0}'.format(col))
        df = df.sort_values(col, ascending=False)
        players = df['player'][:players_in_graph]
        # print(players)
        player_colors = []
        for player in players:
            if player == chosen_player:
                player_colors.append('orangered')
            else:
                player_colors.append('deepskyblue')
        plt.style.use('fivethirtyeight')
        first_player = list(players)[0]
        title = '{0} {1}'.format(first_player, stats_dict[col][0])
        # title = 'Bergessio fue el segundo con mejor promedio de asistencias del equipo'
        fig, ax = plt.subplots(figsize=(10, 8))
        plt.title(title, weight='bold', loc='left', fontsize=26, color='0.2')
        x = np.arange(1, players_in_graph + 1)
        y = df[col][:players_in_graph]
        plt.bar(x, y, align='center', color=player_colors)
        plt.xticks(
            x,
            players,
            color='0.3',
            fontsize=16,
            # rotation='vertical'
        )
        plt.ylim(0, 1.15 * df[col][:players_in_graph].max())
        ax.set_yticklabels([])
        ax.text(
            0,
            1.10 * df[col][: players_in_graph].max(),
            # 'Tiros totales recibidos',
            '{0}'.format(stats_dict[col][1]),
            color='0.3',
            fontsize=18,
            horizontalalignment='left')
        for n, val in enumerate(y):
            if stats_dict[col][2] > 1:
                value = '{0}%'.format(int(stats_dict[col][3] * val))
            else:
                value = round(val, 2)
            ax.annotate(value,
                        xy=(x[n],
                            val),
                        xytext=(x[n],
                                1.01 * val),
                        verticalalignment='bottom',
                        horizontalalignment='center',
                        color='0.3',
                        fontsize=18)
        plt.show()
