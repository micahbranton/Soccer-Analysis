import requests

from datetime import date, timedelta
from selenium import webdriver

import pandas as pd

from bs4 import BeautifulSoup


def date_range(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield (start_date + timedelta(n)).strftime('%Y%m%d')


def get_games_id(
        start_year,
        start_month,
        start_day,
        end_year,
        end_month,
        end_day, competition):

    games_id = []
    dates = []

    for item in date_range(
        date(
            start_year,
            start_month,
            start_day),
        date(
            end_year,
            end_month,
            end_day)):
        dates.append(item)

    driver = webdriver.Chrome()

    if competition == 'liga':
        link_part = 'arg.1'
    elif competition == 'copa_arg':
        link_part = 'arg.copa'
    elif competition == 'copa_lib':
        link_part = 'conmebol.libertadores'
    elif competition == 'supercopa':
        link_part = 'arg.supercopa'
    elif competition == 'copa_sud':
        link_part = 'conmebol.sudamericana'

    link = 'http://www.espn.com.ar/futbol/resultados/_/liga/{0}/fecha/'.format(
        link_part)
    for day in dates:
        driver.get(link + day)

        game_link_driver = driver.find_elements_by_name(
            '&lpos=soccer:scoreboard:resumen')

        game_links = []

        for i in range(len(game_link_driver)):
            game_links.append(game_link_driver[i].get_attribute('href'))

        for game in game_links:
            games_id.append(game[46:53])

        driver.quit

    return games_id


def teams(id):

    url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    teams_html = soup.find_all("div", {"class": "possession"})

    if teams_html is None or not len(teams_html):
        return None

    def html_to_teams(teams_html):

        for item in teams_html:
            name = item.find_all('span', {"class": "team-name"})

        team_names = [n.contents[0] for n in name]
        home_team_temp = team_names[0]
        away_team_temp = team_names[1]

        # Change Name if Atletico Tucuman

        def change_tuc(team_name):
            if 'Atl Tucum' in team_name:
                team_name_new = 'TUC'
            else:
                team_name_new = team_name
            return team_name_new

        home_team = change_tuc(home_team_temp)
        away_team = change_tuc(away_team_temp)

        return home_team, away_team

    home_team, away_team = html_to_teams(teams_html)

    return home_team, away_team


def html_to_players(html):

    if not len(html) or html is None:
        return None

    players_contents = [p.contents[0] for p in html]

    total_players = []
    home_players = []
    away_players = []

    for player in players_contents:
        strip_player = player.strip()
        if strip_player != '':
            total_players.append(strip_player)

    for num in range(18):
        home_players.append(total_players[num])
    for number in range(18, len(total_players)):
        away_players.append(total_players[number])

    return home_players, away_players


def goals(id):

    url = 'http://www.espn.com.ar/futbol/comentario?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    players_html = soup.find_all("span", {"class": "name"})
    goals_html = soup.find_all("ul", {"data-event-type": "goal"})

    def html_to_scorers(html):

        if not len(html) or html is None:
            return None

        list_html = []

        for tag in html:
            list_html.append(tag.find_all("li"))

        goal_scorers = []

        for content in list_html:
            goal_contents = [p.contents[0] for p in content]
            for scorer in goal_contents:
                goal_scorers.append(scorer.strip())

        return goal_scorers

    def html_to_goal_minutes(html, home_players, away_players):

        minutes_html = []

        for tag in html:
            minutes_html.append(tag.find_all("span"))

        minutes_scored_raw = []

        for content in minutes_html:
            minutes_contents = [p.contents[0] for p in content]
            for minute in minutes_contents:
                minutes_scored_raw.append(minute)

        goals_scored_raw = {}
        goals_scored = {}

        if goal_scorers:
            for i in range(len(goal_scorers)):
                goals_scored_raw[goal_scorers[i]] = minutes_scored_raw[i]

        # goles en tiempo de descuento o en contra

        for key in goals_scored_raw.keys():
            if 'OG' in goals_scored_raw[key]:
                if key in home_players:
                    goals_scored[away_players[0]] = goals_scored_raw[key]
                elif key in away_players:
                    goals_scored[home_players[0]] = goals_scored_raw[key]
            elif '+' in goals_scored_raw[key]:
                index = goals_scored_raw[key].index('+')
                goals_scored[key] = str(int(goals_scored_raw[key][
                                        index - 3:index - 1]) + int(goals_scored_raw[key][index + 1])) + "'"
            else:
                goals_scored[key] = goals_scored_raw[key]

        return goals_scored

    def goal_attribution(goals_scored, home_players, away_players):

        home_goals_raw = []
        away_goals_raw = []

        for key in goals_scored.keys():
            if key in home_players:
                home_goals_raw.append(goals_scored[key])
            elif key in away_players:
                away_goals_raw.append(goals_scored[key])

        home_goals = []
        away_goals = []

        for element in home_goals_raw:
            for i in range(len(element)):
                if element[i] == "'":
                    if element[i - 2] == '(':
                        home_goals.append(int(element[i - 1]))
                    else:
                        home_goals.append(int(element[i - 2:i]))

        for element in away_goals_raw:
            for i in range(len(element)):
                if element[i] == "'":
                    if element[i - 2] == '(':
                        away_goals.append(int(element[i - 1]))
                    else:
                        away_goals.append(int(element[i - 2:i]))

        home_goals_sorted = sorted(home_goals)
        away_goals_sorted = sorted(away_goals)

        return home_goals_sorted, away_goals_sorted

    home_players, away_players = html_to_players(players_html)
    goal_scorers = html_to_scorers(goals_html)
    goals_scored = html_to_goal_minutes(goals_html, home_players, away_players)
    home_goals_sorted, away_goals_sorted = goal_attribution(
        goals_scored, home_players, away_players)

    return home_goals_sorted, away_goals_sorted


def get_players_in_goals(id):

    url = 'http://www.espn.com.ar/futbol/comentario?juegoId=' + str(id)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    players_html = soup.find_all("span", {"class": "name"})
    substitution_times_html = soup.find_all(
        "span", {"data-event-type": "substitution"})
    end_of_game_html = soup.find_all("li", {"data-time": "FT"})
    subs_html = soup.find_all("span")
    red_times_html = soup.find_all("span", {"data-event-type": "red-card"})
    red_html = soup.find_all("div", {"class": "detail"})

    def get_subs_times(substitution_times_html):

        subs_times = [n.contents[0] for n in substitution_times_html]

        for i in range(len(subs_times)):
            if '+' in subs_times[i]:
                index = subs_times[i].index('+')
                subs_times[i] = str(
                    int(subs_times[i][index - 2:index]) + int(subs_times[i][index + 1]))

        for i in range(len(subs_times)):
            subs_times[i] = int(subs_times[i])

        return subs_times

    def end_of_game(end_of_game_html):

        for link in end_of_game_html:
            end_of_game_raw = link.get("data-minute")
            end_of_game = int(end_of_game_raw)

        return end_of_game

    def total_team_played(end_of_game, home_team, away_team):

        team_total_played = {}

        team_total_played[home_team] = end_of_game
        team_total_played[away_team] = end_of_game

        return team_total_played

    def get_subs_names(subs_html):

        subs_in = []
        subs_out = []

        for span in subs_html:
            string_span = str(span)
            if 'En:' in string_span:
                subs_in.append(string_span[27:-7])
                # subs_in.append(string_span[27:-7].decode('utf-8', 'ignore'))
            elif 'Fuera:' in string_span:
                subs_out.append(string_span[50:-7])
                # subs_out.append(string_span[50:-7].decode('utf-8', 'ignore'))

        return subs_in, subs_out

    def get_subs_per_team(home_players, away_players):

        home_subs = 0
        away_subs = 0

        for sub in subs_in:
            if sub in home_players:
                home_subs += 1
            elif sub in away_players:
                away_subs += 1

        return home_subs, away_subs

    def get_players_that_played(
            home_players,
            away_players,
            home_subs,
            away_subs):

        home_players_played = []
        away_players_played = []

        for num in range(11 + home_subs):
            home_players_played.append(home_players[num])
        for number in range(11 + away_subs):
            away_players_played.append(away_players[number])

        return home_players_played, away_players_played

    def get_red_card_times(red_times_html):

        if not len(red_times_html):
            return []

        if not len(red_times_html[0].contents):
            return []

        red_times = [n.contents[0] for n in red_times_html]

        for i in range(len(red_times)):
            if '+' in red_times[i]:
                index = red_times[i].index('+')
                red_times[i] = str(
                    int(red_times[i][index - 2:index]) + int(red_times[i][index + 1]))

        for i in range(len(red_times)):
            red_times[i] = int(red_times[i])

        return red_times

    def get_red_card_names(red_html, red_times):

        if not len(red_times):
            return []

        details_names = [n.contents[0] for n in red_html]

        red_names = []

        for detail in details_names:
            if 'Tarjeta roja' in detail:
                red_card_name = detail[:-16].strip()
                red_names.append(red_card_name)

        return red_names

    def time_per_player(
            home_players_played,
            away_players_played,
            end_of_game,
            subs_in,
            subs_out,
            red_times,
            red_names):

        players_time = {}

        for player in home_players_played:
            players_time[player] = end_of_game

        for player in away_players_played:
            players_time[player] = end_of_game

        for i in range(len(subs_in)):
            player_in = subs_in[i]
            player_out = subs_out[i]
            time = int(subs_times[i])
            players_time[player_in] = end_of_game - time
            players_time[player_out] = time

        for i in range(len(red_names)):
            player_red = red_names[i]
            time = red_times[i]
            players_time[player_red] = time

        return players_time

    def player_in_goal(
            players_time,
            home_players_played,
            away_players_played,
            home_team,
            away_team,
            home_goals_sorted,
            away_goals_sorted,
            end_of_game):

        player_in_goals = {}

        for player in players_time:
            if player in home_players_played:
                player_in_goals[player] = [
                    home_team, 0, 0, players_time[player]]
            elif player in away_players_played:
                player_in_goals[player] = [
                    away_team, 0, 0, players_time[player]]

        if len(home_goals_sorted):
            for goal in home_goals_sorted:
                for player in players_time:
                    if goal < players_time[
                            player] or end_of_game - goal < players_time[player]:
                        if player in home_players_played:
                            player_in_goals[player][1] += 1
                        elif player in away_players_played:
                            player_in_goals[player][2] += 1

        if len(away_goals_sorted):
            for goal in away_goals_sorted:
                for player in players_time:
                    if goal < players_time[
                            player] or end_of_game - goal < players_time[player]:
                        if player in home_players_played:
                            player_in_goals[player][2] += 1
                        elif player in away_players_played:
                            player_in_goals[player][1] += 1

        return player_in_goals

    teams_temp = teams(id)
    if teams_temp is None:
        return None
    home_team, away_team = teams(id)
    if html_to_players(players_html) is None:
        return None
    home_players, away_players = html_to_players(players_html)
    home_goals_sorted, away_goals_sorted = goals(id)
    subs_times = get_subs_times(substitution_times_html)
    end_of_game = end_of_game(end_of_game_html)
    subs_in, subs_out = get_subs_names(subs_html)
    home_subs, away_subs = get_subs_per_team(home_players, away_players)
    home_players_played, away_players_played = get_players_that_played(
        home_players, away_players, home_subs, away_subs)
    if id == '440385':
        red_times = [44, 52]
        red_names = [home_players[4], away_players[4]]
    else:
        red_times = get_red_card_times(red_times_html)
        red_names = get_red_card_names(red_html, red_times)

    players_time = time_per_player(
        home_players_played,
        away_players_played,
        end_of_game,
        subs_in,
        subs_out,
        red_times,
        red_names)
    player_in_goals = player_in_goal(
        players_time,
        home_players_played,
        away_players_played,
        home_team,
        away_team,
        home_goals_sorted,
        away_goals_sorted,
        end_of_game)
    team_total_played = total_team_played(end_of_game, home_team, away_team)
    team_goal_difference = {}
    team_goal_difference[home_team] = [
        len(home_goals_sorted),
        len(away_goals_sorted)]
    team_goal_difference[away_team] = [
        len(away_goals_sorted),
        len(home_goals_sorted)]

    return player_in_goals, team_total_played, team_goal_difference


def get_players_data(games_id):

    total_players_goals = {}
    total_team_data = {}
    for game in games_id:
        print(game)
        if get_players_in_goals(game) is not None:
            player_data, team_time, team_goal_difference = get_players_in_goals(
                game)
            for team in team_time.keys():
                if team in total_team_data:
                    total_team_data[team][0] += team_time[team]
                    total_team_data[team][1] += team_goal_difference[team][0]
                    total_team_data[team][2] += team_goal_difference[team][1]
                else:
                    total_team_data[team] = [
                        team_time[team],
                        team_goal_difference[team][0],
                        team_goal_difference[team][1]]
            for player in player_data.keys():
                if player in total_players_goals.keys():
                    total_players_goals[player][1] += player_data[player][1]
                    total_players_goals[player][2] += player_data[player][2]
                    total_players_goals[player][3] += player_data[player][3]
                else:
                    total_players_goals[player] = player_data[player]
    return total_players_goals, total_team_data


def get_dict_with_minutes_in_bench(d1, d2):

    for player in d1.keys():
        for team in d2.keys():
            if d1[player][0] == team:
                d1[player].append(d2[team][0] - d1[player][3])
                d1[player].append(d2[team][1])
                d1[player].append(d2[team][2])

    return d1


def dict_to_list(d):

    dictlist = []
    for key, value in d.items():
        temp = [
            key.encode(
                'ASCII',
                'replace'),
            value[0],
            value[1],
            value[2],
            value[3],
            value[4],
            value[5],
            value[6]]
        dictlist.append(temp)

    return dictlist

# Program
total_games = []
competitions = ['liga', 'copa_lib', 'copa_sud']
for comp in competitions:
    games_id = get_games_id(2016, 2, 5, 2016, 9, 26, comp)
    total_games += games_id

total_players_data, total_team_data = get_players_data(total_games)

total_data = get_dict_with_minutes_in_bench(
    total_players_data, total_team_data)

players_data_list = dict_to_list(total_data)

col_names = [
    'player',
    'team',
    'goals_for',
    'goals_against',
    'minutes_played',
    'minutes_benched',
    'team_goals_for',
    'team_goals_against']

total_data = pd.DataFrame(columns=col_names)

for data in players_data_list:
    total_data.loc[len(total_data)] = data

total_data['team_goals'] = total_data[
    'team_goals_for'] - total_data['goals_for']
total_data['ag_team_goals'] = total_data[
    'team_goals_against'] - total_data['goals_against']

total_data['90m_player_goals'] = 90 * \
    total_data['goals_for'] / total_data['minutes_played']

total_data['ag_90m_player_goals'] = 90 * \
    total_data['goals_against'] / total_data['minutes_played']

total_data['90m_team_goals'] = 90 * \
    total_data['team_goals'] / total_data['minutes_benched']

total_data['ag_90m_team_goals'] = 90 * \
    total_data['ag_team_goals'] / total_data['minutes_benched']

total_data = total_data.fillna(0)

path = 'player_in_goals_2016_9_26.csv'.format(comp)

total_data.to_csv(path, index=False)
