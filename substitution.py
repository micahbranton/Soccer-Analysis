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

def get_players_goals (id):

    url = 'http://www.espn.com.ar/futbol/comentario?juegoId=' + str(id)

    print id

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

# Goals

    goals_html = soup.find_all("ul", {"data-event-type":"goal"})

    list_html = []

    for tag in goals_html:
        list_html.append(tag.find_all("li"))

    goal_scorers = []

    for content in list_html:
        goal_contents = [ p.contents[0] for p in content ]
        for scorer in goal_contents:
            goal_scorers.append(scorer.strip())

    def correcting_name(player):
        if player[-1] in 'abcdefghijklmnopqrstuvwxyz':
            return player
        else:
            new_name = player[:-1]
            return correcting_name(new_name)

    for i in range(len(goal_scorers)):
        goal_scorers[i] = correcting_name(goal_scorers[i])

    minutes_html = []

    for tag in goals_html:
        minutes_html.append(tag.find_all("span"))

    minutes_scored_raw = []

    for content in minutes_html:
        minutes_contents = [ p.contents[0] for p in content ]
        for minute in minutes_contents:
            minutes_scored_raw.append(minute)

    goals_scored_raw = {}
    goals_scored = {}

    for i in range (len(goal_scorers)):
        goals_scored_raw[goal_scorers[i]] = minutes_scored_raw[i]

    # goles en tiempo de descuento

    for key in goals_scored_raw.keys():
        if 'OG' in goals_scored_raw[key]:
            return None

        elif '+' in goals_scored_raw[key]:
            index = goals_scored_raw[key].index('+')
            goals_scored[key] = str(int(goals_scored_raw[key][index-3:index-1]) + int(goals_scored_raw[key][index+1])) + "'"
        else:
            goals_scored[key] = goals_scored_raw[key]

    #jugadores

    players_html = soup.find_all("span", {"class":"name"})

    players_contents = [p.contents[0] for p in players_html]

    home_players = []
    away_players = []

    for num in range(18):
        home_players.append(players_contents[num].strip())
    for number in range(18,len(players_contents)):
        away_players.append(players_contents[number].strip())

    # Goals

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
                if element[i-2] == '(':
                     home_goals.append(int(element[i-1]))
                else:
                    home_goals.append(int(element[i-2:i]))

    for element in away_goals_raw:
        for i in range(len(element)):
            if element[i] == "'":
                if element[i-2] == '(':
                     away_goals.append(int(element[i-1]))
                else:
                    away_goals.append(int(element[i-2:i]))

    home_goals_sorted = sorted(home_goals)
    away_goals_sorted = sorted(away_goals)

    # Substitute Times

    substitution_times_html = soup.find_all("span", {"data-event-type":"substitution"})

    subs_times = [n.contents[0] for n in substitution_times_html]

    for i in range(len(subs_times)):
        if '+' in subs_times[i]:
            index = subs_times[i].index('+')
            subs_times[i] = str(int(subs_times[i][index-2:index]) + int(subs_times[i][index+1]))

    for i in range(len(subs_times)):
        subs_times[i] = int(subs_times[i])

    # End of Game

    end_of_game_html = soup.find_all("li", {"data-time":"FT"})

    for link in end_of_game_html:
        end_of_game_raw = link.get("data-minute")
        end_of_game = int(end_of_game_raw)

    # Substitute Names
    
    total_span_html = soup.find_all("span")

    subs_in = []
    subs_out = []

    for span in total_span_html:
        string_span = str(span)
        if 'En:' in string_span:
            subs_in.append(string_span[27:-7].decode('utf-8', 'ignore'))
        elif 'Fuera:' in string_span:
            subs_out.append(string_span[50:-7].decode('utf-8', 'ignore'))

    home_subs = 0
    away_subs = 0

    for sub in subs_in:
        if sub in home_players:
            home_subs += 1
        elif sub in away_players:
            away_subs +=1

    # Red Card Times

    red_times_html = soup.find_all("span", {"data-event-type":"red-card"})

    red_times = [n.contents[0] for n in red_times_html]

    for i in range(len(red_times)):
        if '+' in red_times[i]:
            index = red_times[i].index('+')
            red_times[i] = str(int(red_times[i][index-2:index]) + int(red_times[i][index+1]))

    for i in range(len(red_times)):
        red_times[i] = int(red_times[i])

    # Red Card Names

    details_html = soup.find_all("div", {"class":"detail"})

    details_names = [n.contents[0] for n in details_html]

    red_names = []

    for detail in details_names:
        if 'Tarjeta roja' in detail:
            red_card_name = detail[:-16].strip()
            red_names.append(red_card_name)

    # Players that played

    home_players_played = []
    away_players_played = []

    for num in range(11 + home_subs):
        home_players_played.append(home_players[num])
    for number in range(11 + away_subs):
        away_players_played.append(away_players[number])

    # Time played by each players

    players_time = {}

    for player in home_players_played:
        players_time[player] = end_of_game

    for player in away_players_played:
        players_time[player] = end_of_game

    for i in range(len(subs_in)):
        player_in = subs_in[i]
        player_out = subs_out[i]
        time = int(subs_times[i])
        players_time [player_in] = end_of_game - time
        players_time [player_out] = time

    for i in range(len(red_names)):
        player_red = red_names[i]
        time = red_times[i]
        players_time [player_red] = time

    # Player in goal

    player_goals = {}

    for player in players_time:
        player_goals [player] = [0,0,players_time[player]]

    if len(home_goals_sorted):
        for goal in home_goals_sorted:
            for player in players_time:
                if goal < players_time[player] or end_of_game - goal < players_time[player]:
                    if player in home_players:
                        player_goals[player][0] += 1
                    elif player in away_players:
                        player_goals[player][1] += 1

    if len(away_goals_sorted):
        for goal in away_goals_sorted:
            for player in players_time:
                if goal < players_time[player] or end_of_game - goal < players_time[player]:
                    if player in home_players_played:
                        player_goals[player][1] += 1
                    elif player in away_players_played:
                        player_goals[player][0] += 1

    return player_goals

def get_players_data(games_id):
    total_players_goals = {}
    for game in games_id:
        data = get_players_goals(game)
        for player in data.keys():
            if player in total_players_goals.keys():
                total_players_goals[player][0] += data[player][0]
                total_players_goals[player][1] += data[player][1]
                total_players_goals[player][2] += data[player][2]
            else:
                total_players_goals[player] = data[player]
    return total_players_goals

def dict_to_list(d):
    dictlist = []
    for key, value in d.items():
        temp = [key.encode('ASCII','replace'),value[0], value[1],value[2]]
        dictlist.append(temp)
    return dictlist

def write_to_csv (games):
      writer = csv.writer(csv_file)
      writer.writerows(games)

# Program

games_id = get_games_id (2016, 4, 30, 2016, 5, 2)

total_players_data = get_players_data(games_id)

players_data_list = dict_to_list(total_players_data)

row_names = ['player', 'goals_for', 'goals_against', 'minutes_played']

with open('player_data.csv', 'w') as csv_file:
    write_to_csv([row_names])

    for player in players_data_list:
        write_to_csv([player])



