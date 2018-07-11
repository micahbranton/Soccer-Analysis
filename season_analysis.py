# =============================================================================
#          File: season_analysis.py
#        Author: Andre Brener
#       Created: 21 Dec 2016
# Last Modified: 29 Sep 2017
#   Description: description
# =============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.style.use('fivethirtyeight')

df = pd.read_csv(os.path.join('data', 'game_data', 'games_data_2016-08-26_2016-12-19.csv'))

# print(df.columns)

df['game_count'] = 1

home_stats = df.groupby('home_name').sum().reset_index()
away_stats = df.groupby('away_name').sum().reset_index()


def get_stats_attribution(col_list, game_state):
    new_col_list = []
    if game_state == 'home':
        state = ['_for', '_against']
    else:
        state = ['_against', '_for']
    for col in col_list:
        if 'home' in col:
            col_name = col[5:] + state[0]
        elif 'away' in col:
            col_name = col[5:] + state[1]
        else:
            col_name = col
        new_col_list.append(col_name)
    new_col_list[0] = 'team_name'
    return new_col_list


# print(get_stats_attribution(home_stats.columns, 'home'))

home_stats.columns = get_stats_attribution(home_stats.columns, 'home')
away_stats.columns = get_stats_attribution(away_stats.columns, 'away')

# print(home_stats.head())
# print(away_stats.head())

total_stats = home_stats.append(away_stats)
team_stats = total_stats.groupby('team_name').sum().reset_index()

shot_stats = team_stats[[
    'team_name', 'goals_for', 'goals_against', 'totalshots_for',
    'totalshots_against', 'shotsgoal_for', 'shotsgoal_against'
]]

shot_stats['tsr'] = shot_stats['totalshots_for'] / \
    (shot_stats['totalshots_for'] + shot_stats['totalshots_against'])

shot_stats['sotr'] = shot_stats['shotsgoal_for'] / \
    (shot_stats['shotsgoal_for'] + shot_stats['shotsgoal_against'])

shot_stats['shot_accuracy_for'] = shot_stats['shotsgoal_for'] / shot_stats[
    'totalshots_for']

shot_stats['shot_accuracy_against'] = shot_stats[
    'shotsgoal_against'] / shot_stats['totalshots_against']

shot_stats['goal_conversion_for'] = shot_stats['goals_for'] / shot_stats[
    'shotsgoal_for']

shot_stats['goal_conversion_against'] = shot_stats[
    'goals_against'] / shot_stats['shotsgoal_against']

# shot_stats = shot_stats[['team_name',
# 'tsr',
# 'sotr',
# 'shot_accuracy_for',
# 'shot_accuracy_against',
# 'goal_conversion_for',
# 'goal_conversion_against']]

teams_in_graph = 5
chosen_team = 'CABJ'

stats_dict = {
    'goals_for': [
        'es el más goleador del Torneo',
        'Top {0} de Equipos con más goles a favor'.format(teams_in_graph),
        False, 1
    ],
    'goals_against': [
        'es el que menos goles le convirtieron',
        'Top {0} de Equipos con menos goles en contra'.format(teams_in_graph),
        True, 1
    ],
    'totalshots_for': [
        'es el más tirador',
        'Top {0} de Equipos con más tiros a favor'.format(teams_in_graph),
        False, 1
    ],
    'totalshots_against': [
        'es el que menos tiros recibió',
        'Top {0} de Equipos que menos tiros concedieron a sus rivales'.format(
            teams_in_graph), True, 1
    ],
    'shotsgoal_for': [
        'es el más tirador',
        'Top {0} de Equipos con más tiros al arco a favor'.format(
            teams_in_graph), False, 1
    ],
    'shotsgoal_against': [
        'es el que menos tiros al arco recibió',
        'Top {0} de Equipos que menos tiros al arco concedieron a sus rivales'.
        format(teams_in_graph), True, 1
    ],
    'tsr': [
        'es el más Dominador en Tiros Totales',
        'Top {0} de Equipos que más superan a sus rivales en ese ámbito'.
        format(teams_in_graph), False, 1
    ],
    'sotr': [
        'es el más dominador en tiros al arco',
        'Top {0} de Equipos que más superan a sus rivales en ese ámbito'.
        format(teams_in_graph), False, 1
    ],
    'shot_accuracy_for': [
        'tiene el ataque más peligroso',
        'Top {0} de Equipos con mayor proporción de tiros al arco sobre tiros realizados'.
        format(teams_in_graph), False, 100
    ],
    'shot_accuracy_against': [
        'es el que menos tiros al arco recibe',
        'Top {0} de Equipos con menor proporción de tiros al arco sobre tiros recibidos'.
        format(teams_in_graph), True, 100
    ],
    'goal_conversion_for': [
        'tiene el ataque más efectivo',
        'Top {0} de Equipos con mayor proporción de goles convertidos sobre tiros al arco realizados'.
        format(teams_in_graph), False, 100
    ],
    'goal_conversion_against': [
        'tiene la defensa más efectiva',
        'Top {0} de Equipos con menor proporción de goles en contra sobre tiros al arco recibidos'.
        format(teams_in_graph), True, 100
    ],
}

team_dict = {
    'CABJ': 'Boca',
    'CARP': 'River',
    'SL': 'San Lorenzo',
    'ALDO': 'Aldosivi',
    'ARS': 'Arsenal',
    'BAN': 'Banfield',
    'BEL': 'Belgrano',
    'CAP': 'Patronato',
    'COL': 'Colón',
    'DYJ': 'Defensa y Justicia',
    'EST': 'Estudiantes',
    'GCM': 'Godoy Cruz',
    'GLP': 'GELP',
    'HUR': 'Huracán',
    'IND': 'Independiente',
    'LAN': 'Lanús',
    'NOB': 'Newells',
    'OBB': 'Olimpo',
    'QUI': 'Quilmes',
    'RAC': 'Racing',
    'RAF': 'A. Rafaela',
    'ROS': 'R. Central',
    'SARM': 'Sarmiento',
    'SMSJ': 'San Martin SJ',
    'TDC': 'Talleres',
    'TEMP': 'Temperley',
    'TIG': 'Tigre',
    'TUC': 'A. Tucuman',
    'USF': 'Unión',
    'VEL': 'Velez'
}

for col in shot_stats.columns:
    if col != 'team_name':
        # print('\n{0}'.format(col))
        df = shot_stats.sort_values(col, ascending=stats_dict[col][2])
        team_names = []
        team_colors = []
        for team in df['team_name'][:teams_in_graph]:
            name = team_dict[team]
            team_names.append(name)
            if team == chosen_team:
                team_colors.append('orangered')
            else:
                team_colors.append('deepskyblue')

        first_team = team_dict[list(df['team_name'])[0]]
        title = '{0} {1}'.format(first_team, stats_dict[col][0])
        # title = 'Boca es de los equipos que más tiros recibe'
        fig, ax = plt.subplots(figsize=(10, 8))
        plt.title(title, weight='bold', loc='left', fontsize=26, color='0.2')
        x = np.arange(1, teams_in_graph + 1)
        y = df[col][:teams_in_graph]
        plt.bar(x, y, align='center', color=team_colors)
        plt.xticks(
            x,
            team_names,
            color='0.3',
            fontsize=16,
            # rotation='vertical'
        )
        plt.ylim(0, 1.15 * df[col][:teams_in_graph].max())
        ax.set_yticklabels([])
        ax.text(
            0,
            1.10 * df[col][:teams_in_graph].max(),
            # 'Tiros totales recibidos',
            '{0}'.format(stats_dict[col][1]),
            color='0.3',
            fontsize=18,
            horizontalalignment='left')
        for n, val in enumerate(y):
            if stats_dict[col][3] > 1:
                value = '{0}%'.format(int(stats_dict[col][3] * val))
            else:
                value = round(val, 2)
            ax.annotate(
                value,
                xy=(x[n], val),
                xytext=(x[n], 1.01 * val),
                verticalalignment='bottom',
                horizontalalignment='center',
                color='0.3',
                fontsize=18)
        plt.show()

# print(shot_stats)
