import requests
from bs4 import BeautifulSoup

def get_players(id):

    url = 'http://www.espn.com.ar/futbol/comentario?juegoId=' + str(id)

    print id

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    
    #Red Card Times

    total_span_html = soup.find_all("span")

    subs_in = []
    subs_out = []

    for span in total_span_html:
    	string_span = str(span)
    	if 'En:' in string_span:
    		subs_in.append(string_span[27:-7])
    	elif 'Fuera:' in string_span:
    		subs_out.append(string_span[50:-7])

    players_contents = [p.contents[0] for p in players_html]

    home_players_for_goals = []
    away_players_for_goals = []

    for num in range(18):
        home_players_for_goals.append(players_contents[num].strip())
    for number in range(18,len(players_contents)):
        away_players_for_goals.append(players_contents[number].strip())
    


get_players(440409)
