from selenium import webdriver
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import csv

def date_range(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield (start_date + timedelta(n)).strftime('%Y%m%d')

def get_games_id (start_year, start_month, start_day, end_year, end_month, end_day):
    
    games_id = []
    dates = []

    for item in date_range(date(start_year, start_month, start_day), date(end_year, end_month, end_day)):
        dates.append(item)

    driver = webdriver.Chrome()

    for day in dates:
        driver.get('http://www.espn.com.ar/futbol/resultados/_/liga/arg.1/fecha/' + day)

        game_link_driver = driver.find_elements_by_name('&lpos=soccer:scoreboard:resumen')

        game_links = []

        for i in range(len(game_link_driver)):
            game_links.append(game_link_driver[i].get_attribute('href'))

        for game in game_links:
            games_id.append(game[46:53])

        driver.quit

    return games_id

def get_game_data (id):

    print id

    url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    home_html = soup.find_all("span", {"class":"score icon-font-after"})
    away_html = soup.find_all("span", {"class":"score icon-font-before"})
    possession_html = soup.find_all("div", {"class":"possession"})
    teams_html = soup.find_all("div", {"class":"possession"})
    shots_html = soup.find_all("div", {"class":"shots"})
    fouls_html = soup.find_all("td", {"data-stat":"foulsCommitted"})
    yellow_html = soup.find_all("td", {"data-stat":"yellowCards"})
    red_html = soup.find_all("td", {"data-stat":"redCards"})

    def html_to_score (html):

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
            possession_data = item.find_all('span',{"class":"chartValue"})

        pos_contents = [p.contents[0] for p in possession_data]

        possesion_percentage = []

        for content in pos_contents:
            percentage_num = int(content[:-1])
            possesion_percentage.append (percentage_num)

        return possesion_percentage

    def teams (teams_html):

        if not teams_html:
            return None
        for item in teams_html:
            name = item.find_all('span',{"class":"team-name"})

        team_names = [n.contents[0] for n in name]
        home_team_raw = team_names[0]
        away_team_raw = team_names[1]

        if 'Atl Tucum' in home_team_raw:
            home_team = 'TUC'
        else:
            home_team = home_team_raw

        if 'Atl Tucum' in away_team_raw:
            away_team = 'TUC'
        else:
            away_team = away_team_raw

        return home_team, away_team

    def get_shots(shots_html):

        for item in shots_html:
            shots_data = item.find_all('span',{"class":"number"})

        shots_contents = [s.contents[0] for s in shots_data]

        shots_home = shots_contents[0].split()
        shots_away = shots_contents[1].split()

        shots_home_nobrackets = shots_home[1][1:-1]
        shots_away_nobrackets = shots_away[1][1:-1]

        shots_home_num = [int(shots_home[0]),int(shots_home_nobrackets)]
        shots_away_num = [int(shots_away[0]),int(shots_away_nobrackets)]

        shots_total = [shots_home_num[0],shots_away_num[0]]
        shots_ongoal = [shots_home_num[1],shots_away_num[1]]

        return shots_total, shots_ongoal

    def get_fouls(fouls_html):

        fouls_contents = [p.contents[0] for p in fouls_html]

        fouls = []

        for foul in fouls_contents:
            fouls_num = int(foul)
            fouls.append (fouls_num)

        return fouls

    def get_cards(cards_html):

        cards_content = [p.contents[0] for p in cards_html]

        cards = []

        for i in cards_content:
            cards_num = int(i)
            cards.append (cards_num)

        return cards

    home_goals = html_to_score(home_html)
    away_goals = html_to_score(away_html)
    possesion_percentage = get_possesion_values(possession_html)
    home_team, away_team = teams(teams_html)
    shots_total, shots_ongoal = get_shots(shots_html)
    fouls = get_fouls(fouls_html)
    yellow = get_cards(yellow_html)
    red = get_cards(red_html)

    game = [home_team, away_team, home_goals, away_goals,
            shots_total[0], shots_total[1], shots_ongoal[0], shots_ongoal[1],
            possesion_percentage[0], possesion_percentage[1],
            fouls[0], fouls[1], yellow[0], yellow[1], red[0], red[1]]

    return game

def get_penalties(id):

    url = 'http://www.espn.com.ar/futbol/partido?juegoId='+ str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    resumen_html = soup.find_all("div", {"class":"detail"})
    players_html = soup.find_all("span", {"class":"name"})

    def get_penalty_shooters(resumen_html):

        resumen_contents = [p.contents[0] for p in resumen_html]

        if resumen_contents[0] == '\n':
            return None

        resumen_contents_strip = []

        for item in resumen_contents: 
            strip = item.strip()
            resumen_contents_strip.append(strip)

        penalty_contents = []

        for item in resumen_contents_strip:
            if 'Penalty' in item:
                penalty_contents.append(item)

        shooters = []

        for i in range(len(penalty_contents)):
            inter = penalty_contents[i].split()
            shooters.append(inter[0] + ' ' + inter[1])

        return shooters

    def html_to_players(html):

        if not len(html):
            return None

        players_contents = [ p.contents[0] for p in html ]

        home_players = []
        away_players = []

        for num in range(18):
            home_players.append(players_contents[num].strip())
        for number in range(18,len(players_contents)):
            away_players.append(players_contents[number].strip())

        return home_players, away_players

    def penalty_attribution(shooters,home_players, away_players):

        home_penalties = 0
        away_penalties = 0

        for shooter in shooters:
            if shooter in home_players:
                home_penalties +=1
            elif shooter in away_players:
                away_penalties += 1

        return home_penalties, away_penalties

    shooters = get_penalty_shooters(resumen_html)
    home_players, away_players = html_to_players(players_html)
    home_penalties, away_penalties = penalty_attribution(shooters,home_players,away_players)

    return home_penalties, away_penalties

def write_to_csv (games):
      writer = csv.writer(csv_file)
      writer.writerows(games)

def get_match_data (games_id):
    list_of_games_data = []

    for game in games_id:
        game_data = get_game_data(game)
        home_penalties, away_penalties = get_penalties(game)
        game_data.append(home_penalties)
        game_data.append(away_penalties)
        if game_data:
            list_of_games_data.append(game_data)

    return list_of_games_data

# Program
games_id = get_games_id (2016, 5, 6, 2016, 5, 7)

list_of_games_data = get_match_data(games_id)

row_names = ['home_name', 'away_name', 'home_goals', 'away_goals',
        'home_totalshots', 'away_totalshots','home_shotsgoal', 'away_shotsgoal',
        'home_possession', 'away_possesion','home_fouls', 'away_fouls',
        'home_yellow', 'away_yellow', 'home_red', 'away_red','home_penalties', 'away_penalties']

with open('games_data.csv', 'w') as csv_file:
    write_to_csv([row_names])

    for game in list_of_games_data:
        write_to_csv([game])
