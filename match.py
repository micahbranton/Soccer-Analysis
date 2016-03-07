import requests
from bs4 import BeautifulSoup

for id in  match_id:

	url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')

#home score
home_html = soup.find_all("span", {"class":"score icon-font-after"})

home_contents = [ p.contents[0] for p in home_html ]

home_goals = int(home_contents[0].strip())

#away score
away_html = soup.find_all("span", {"class":"score icon-font-before"})

away_contents = [ p.contents[0] for p in away_html ]

away_goals = int(away_contents[0].strip())

#porcentaje de posesion
	possession_html = soup.find_all("div", {"class":"possession"})

	for item in possession_html:
		possession_data = item.find_all('span',{"class":"chartValue"})

	pos_contents = [ p.contents[0] for p in possession_data ]

	possesion_percentage = []

	for content in pos_contents:
		percentage_num = int(content[:-1])
		possesion_percentage.append (percentage_num)

	#nombre de equipos
	for item in possession_html:
		name = item.find_all('span',{"class":"team-name"})

	team_names = [ n.contents[0] for n in name ]

	#shots
	shots_html = soup.find_all("div", {"class":"shots"})

	for item in shots_html:
		shots_data = item.find_all('span',{"class":"number"})

	shots_contents = [ s.contents[0] for s in shots_data ]

	shots_home = shots_contents[0].split()
	shots_away = shots_contents[1].split()

	shots_home_nobrackets = shots_home[1][1:-1]
	shots_away_nobrackets = shots_away[1][1:-1]

	shots_home_num = [int(shots_home[0]),int(shots_home_nobrackets)]
	shots_away_num = [int(shots_away[0]),int(shots_away_nobrackets)]

	shots_total = [shots_home_num[0],shots_away_num[0]]
	shots_ongoal = [shots_home_num[1],shots_away_num[1]]

	#cantidad de fouls
	fouls_html = soup.find_all("td", {"data-stat":"foulsCommitted"})

	fouls_contents = [ p.contents[0] for p in fouls_html ]

	fouls = []

	for i in fouls_contents:
		fouls_num = int(i)
		fouls.append (fouls_num)

	#amarillas
	yellow_html = soup.find_all("td", {"data-stat":"yellowCards"})

	yellow_contents = [ p.contents[0] for p in yellow_html ]

	yellow = []

	for i in yellow_contents:
		yellow_num = int(i)
		yellow.append (yellow_num)

	#rojas
	red_html = soup.find_all("td", {"data-stat":"redCards"})

	red_contents = [ p.contents[0] for p in red_html ]

	red = []

	for i in red_contents:
		red_num = int(i)
		red.append (red_num)

	#penales

	url = 'http://www.espn.com.ar/futbol/partido?juegoId='+ str(id)

	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')

	resumen_html = soup.find_all("div", {"class":"detail"})

	resumen_contents = [ p.contents[0] for p in resumen_html ]

	resumen_contents_strip = []

	for item in resumen_contents: 
		strip = item.strip()
		resumen_contents_strip.append(strip)

	penalty_contents =[]

	for item in resumen_contents_strip:
		if 'Penalty' in item:
			penalty_contents.append(item)

	shooters = []
	#pateador del penal
	for i in range(len(penalty_contents)):
		inter = penalty_contents[i].split()
		shooters.append(inter[0] + ' ' + inter[1])

	#jugadores
	players_html = soup.find_all("span", {"class":"name"})

	players_contents = [ p.contents[0] for p in players_html ]

	home_players = []
	away_players = []

	for num in range(18):
		home_players.append(players_contents[num].strip())
	for number in range(18,36):
		away_players.append(players_contents[number].strip())


	#de quien fue el penal

	home_penalties = 0
	away_penalties = 0


	for shooter in shooters:
		if shooter in home_players:
			home_penalties +=1
		else:
			away_penalties += 1


	match = {'home':team_names[0], 'away':team_names[1], 'pos_home':possesion_percentage[0], 'pos_away':possesion_percentage[1],
	'shots_total_home':shots_total[0], 'shots_total_away':shots_total[1], 'yellow_home':yellow[0], 'yellow_away':yellow[1],
	'red_home':red[0], 'red_away':red[1], 'home_penalties':home_penalties, 'away_penalties':away_penalties,'shots_ongoal_home':shots_ongoal[0],
	'shots_ongoal_away':shots_ongoal[1],'goals_home':home_goals,'goals_away':away_goals}

	print match