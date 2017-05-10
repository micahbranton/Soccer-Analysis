import os
import csv

from datetime import date, timedelta

import requests

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def date_range(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield (start_date + timedelta(n)).strftime('%Y%m%d')


def get_games_id(start_date, end_date):

    dates = [d for d in date_range(start_date, end_date)]

    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    driver = Chrome(chrome_options=chrome_options)

    for day in dates:
        driver.get(
            'http://www.espn.com.ar/futbol/resultados/_/liga/arg.1/fecha/' +
            day)

        game_link_driver = driver.find_elements_by_class_name(
            'mobileScoreboardLink  ')

        game_links = []

        for i in range(len(game_link_driver)):
            # print(game_link_driver[i].get_attribute('href'))
            game_links.append(game_link_driver[i].get_attribute('href'))

        games_id = [game[46:53] for game in game_links]

        driver.quit

    # print(games_id)
    return games_id


def get_score(html):

    if not len(html):
        return None

    contents = [p.contents[0] for p in html]
    score_string = (contents[0].strip())

    if not len(score_string):
        return None

    score = int(score_string)
    return score


def get_possesion_values(possession_html):

    if not len(possession_html):
        return None

    for item in possession_html:
        possession_data = item.find_all('span', {"class": "chartValue"})

    pos_contents = [p.contents[0] for p in possession_data]

    pos_percentage = [int(item[:-1]) for item in pos_contents]

    return pos_percentage


def get_teams(teams_html):

    if not teams_html:
        return None

    for item in teams_html:
        name = item.find_all('span', {"class": "team-name"})

    team_names = [n.contents[0] for n in name]

    for team in team_names:
        if 'Atl Tucum' in team:
            team = 'TUC'

    return team_names


def split_shots(shots):
    shots = shots.split()
    total_shots = int(shots[0])
    sot = int(shots[1][1:-1])
    return total_shots, sot


def get_shots(shots_html):

    if not len(shots_html):
        return None

    for item in shots_html:
        shots_data = item.find_all('span', {"class": "number"})

    shots_contents = [s.contents[0] for s in shots_data]

    home_shots, home_sot = split_shots(shots_contents[0])
    away_shots, away_sot = split_shots(shots_contents[1])

    shots_total = [home_shots, away_shots]
    shots_ongoal = [home_sot, away_sot]

    return [shots_total, shots_ongoal]


def get_fouls(fouls_html):

    fouls_contents = [p.contents[0] for p in fouls_html]

    fouls = [int(foul) for foul in fouls_contents]

    return fouls


def get_cards(cards_html):

    cards_content = [p.contents[0] for p in cards_html]

    cards = [int(i) for i in cards_content]

    return cards


def get_game_data(id):

    print(id)

    url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    home_html = soup.find_all("span", {"class": "score icon-font-after"})
    away_html = soup.find_all("span", {"class": "score icon-font-before"})
    possession_html = soup.find_all("div", {"class": "possession"})
    teams_html = soup.find_all("div", {"class": "possession"})
    shots_html = soup.find_all("div", {"class": "shots"})
    fouls_html = soup.find_all("td", {"data-stat": "foulsCommitted"})
    yellow_html = soup.find_all("td", {"data-stat": "yellowCards"})
    red_html = soup.find_all("td", {"data-stat": "redCards"})

    home_goals = get_score(home_html)
    away_goals = get_score(away_html)
    pos_percentage = get_possesion_values(possession_html)
    teams = get_teams(teams_html)
    shots = get_shots(shots_html)
    fouls = get_fouls(fouls_html)
    yellow = get_cards(yellow_html)
    red = get_cards(red_html)

    if not teams or not pos_percentage:
        return None

    game = [
        teams[0], teams[1], home_goals, away_goals, shots[0][0], shots[0][1],
        shots[1][0], shots[1][1], pos_percentage[0], pos_percentage[1],
        fouls[0], fouls[1], yellow[0], yellow[1], red[0], red[1]
    ]

    return game


def get_penalty_shooters(summary_html):

    if not len(summary_html):
        return None

    s_contents = [p.contents[0] for p in summary_html]

    if s_contents[0] == '\n':
        return None

    temp_contents = [i.strip() for i in s_contents]

    penalty_contents = [i for i in temp_contents if 'penalty' in i.lower()]

    shooters = []

    for item in penalty_contents:
        temp = item.split()
        shooters.append(temp[0] + ' ' + temp[1])

    return shooters


def get_players(players_html):

    if not len(players_html):
        return None

    pl_contents = [p.contents[0] for p in players_html]

    pl_contents = [i.strip() for i in pl_contents if len(i.strip()) > 0]

    home_players = [pl for pl in pl_contents[:18]]
    away_players = [pl for pl in pl_contents[18:]]

    return [home_players, away_players]


def penalty_attribution(shooters, home_players, away_players):

    home_penalties = 0
    away_penalties = 0

    for shooter in shooters:
        if shooter in home_players:
            home_penalties += 1
        elif shooter in away_players:
            away_penalties += 1

    return home_penalties, away_penalties


def get_penalties(id):

    url = 'http://www.espn.com.ar/futbol/partido?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    summary_html = soup.find_all("div", {"class": "detail"})
    players_html = soup.find_all("span", {"class": "name"})

    shooters = get_penalty_shooters(summary_html)
    players = get_players(players_html)

    if not players:
        return None

    home_players, away_players = players

    home_penalties, away_penalties = penalty_attribution(
        shooters, home_players, away_players)

    return [home_penalties, away_penalties]


def write_to_csv(games, csv_file):
    writer = csv.writer(csv_file)
    writer.writerows(games)


def run_game_data(games_id):
    list_of_games_data = []

    for game in games_id:
        game_data = get_game_data(game)
        hp = 0
        ap = 0
        penalties = get_penalties(game)
        if penalties:
            hp = penalties[0]
            ap = penalties[1]
            game_data.append(hp)
            game_data.append(ap)
        if game_data:
            list_of_games_data.append(game_data)

    return list_of_games_data


def main(start_date, end_date, row_names):

    games_id = get_games_id(start_date, end_date)
    list_of_games_data = run_game_data(games_id)

    os.makedirs('data', exist_ok=True)
    with open('games_data_{}_{}.csv'.format(start_date, end_date),
              'w') as csv_file:
        write_to_csv([row_names], csv_file)

        for game in list_of_games_data:
            write_to_csv([game, csv_file])


if __name__ == '__main__':

    # get_game_data()

    start_date = date(2017, 5, 7)
    end_date = date(2017, 5, 8)

    row_names = [
        'home_name', 'away_name', 'home_goals', 'away_goals',
        'home_totalshots', 'away_totalshots', 'home_shotsgoal',
        'away_shotsgoal', 'home_possession', 'away_possession', 'home_fouls',
        'away_fouls', 'home_yellow', 'away_yellow', 'home_red', 'away_red',
        'home_penalties', 'away_penalties'
    ]

    main(start_date, end_date, row_names)
