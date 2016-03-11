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

    url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    # Home Score
    home_html = soup.find_all("span", {"class":"score icon-font-after"})
    if not len(home_html):
        return None

    home_contents = [p.contents[0] for p in home_html]

    home_goals = int(home_contents[0].strip())

    # Away Score
    away_html = soup.find_all("span", {"class":"score icon-font-before"})

    away_contents = [p.contents[0] for p in away_html]

    away_goals = int(away_contents[0].strip())

    # Possession Percentage
    possession_html = soup.find_all("div", {"class":"possession"})

    for item in possession_html:
        possession_data = item.find_all('span',{"class":"chartValue"})

    pos_contents = [p.contents[0] for p in possession_data]

    possesion_percentage = []

    for content in pos_contents:
        percentage_num = int(content[:-1])
        possesion_percentage.append (percentage_num)

    # Team Names
    for item in possession_html:
        name = item.find_all('span',{"class":"team-name"})

    team_names = [n.contents[0] for n in name]

    # Shots
    shots_html = soup.find_all("div", {"class":"shots"})

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

    # Fouls
    fouls_html = soup.find_all("td", {"data-stat":"foulsCommitted"})

    fouls_contents = [p.contents[0] for p in fouls_html]

    fouls = []

    for foul in fouls_contents:
        fouls_num = int(foul)
        fouls.append (fouls_num)

    # Yellow Cards
    yellow_html = soup.find_all("td", {"data-stat":"yellowCards"})

    yellow_contents = [p.contents[0] for p in yellow_html]

    yellow = []

    for i in yellow_contents:
        yellow_num = int(i)
        yellow.append (yellow_num)

    # Red Cards
    red_html = soup.find_all("td", {"data-stat":"redCards"})

    red_contents = [ p.contents[0] for p in red_html ]

    red = []

    for i in red_contents:
        red_num = int(i)
        red.append (red_num)

    # Penalties

    url = 'http://www.espn.com.ar/futbol/partido?juegoId='+ str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    resumen_html = soup.find_all("div", {"class":"detail"})

    resumen_contents = [p.contents[0] for p in resumen_html]

    resumen_contents_strip = []

    for item in resumen_contents: 
        strip = item.strip()
        resumen_contents_strip.append(strip)

    penalty_contents = []

    for item in resumen_contents_strip:
        if 'Penalty' in item:
            penalty_contents.append(item)

    shooters = []

    # Penalty Shooter
    for i in range(len(penalty_contents)):
        inter = penalty_contents[i].split()
        shooters.append(inter[0] + ' ' + inter[1])

    # Players
    players_html = soup.find_all("span", {"class":"name"})

    players_contents = [p.contents[0] for p in players_html]

    home_players = []
    away_players = []

    for num in range(18):
        home_players.append(players_contents[num].strip())
    for number in range(18,36):
        away_players.append(players_contents[number].strip())

    # Penalty Attribution
    home_penalties = 0
    away_penalties = 0

    for shooter in shooters:
        if shooter in home_players:
            home_penalties +=1
        else:
            away_penalties += 1

    # [home_name, away_name, home_goals, away_goals, home_penalties, away_penalties, home_totalshots, away_totalshots,
    # home_shotsgoal, away_shotsgoal, home_possession, away_possesion, home_yellow, away_yellow, home_red, away_red]
        
    game = [team_names[0], team_names[1], home_goals, away_goals,
            home_penalties, away_penalties, shots_total[0], shots_total[1],
            shots_ongoal[0], shots_ongoal[1],possesion_percentage[0], possesion_percentage[1],
            yellow[0], yellow[1], red[0], red[1]]

    return game

def write_to_csv (games):
      writer = csv.writer(csv_file)
      writer.writerows(games)

# Program
games_id = get_games_id (2016, 3, 5, 2016, 3, 7)

list_of_games_data = []

for game in games_id:
    game_data = get_game_data(game)
    if game_data:
        list_of_games_data.append(game_data)

row_names = ['home_name', 'away_name', 'home_goals', 'away_goals',
        'home_penalties', 'away_penalties', 'home_totalshots', 'away_totalshots',
        'home_shotsgoal', 'away_shotsgoal', 'home_possession', 'away_possesion',
        'home_yellow', 'away_yellow', 'home_red', 'away_red']

with open('games_data.csv', 'w') as csv_file:
    write_to_csv([row_names])

    for game in list_of_games_data:
        write_to_csv([game])
