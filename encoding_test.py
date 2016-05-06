import requests
from bs4 import BeautifulSoup

def get_players(id):

    url = 'http://www.espn.com.ar/futbol/comentario?juegoId=' + str(id)

    print id

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    
    # Cambios

    total_span_html = soup.find_all("span")

    subs_in = []
    subs_out = []

    for span in total_span_html:
    	string_span = str(span)
    	if 'En:' in string_span:
    		subs_in.append(string_span[27:-7])
    	elif 'Fuera:' in string_span:
    		subs_out.append(string_span[50:-7])

    print subs_in

    # Jugadores 1

    players_contents = [p.contents[0] for p in players_html]

    home_players_for_goals = []
    away_players_for_goals = []

    for num in range(18):
        home_players_for_goals.append(players_contents[num].strip())
    for number in range(18,len(players_contents)):
        away_players_for_goals.append(players_contents[number].strip())

    print home_players_for_goals

    # Red Card Names

    details_html = soup.find_all("div", {"class":"detail"})

    details_names = [n.contents[0] for n in details_html]

    red_names = []

    for detail in details_names:
        if 'Tarjeta roja' in detail:
            red_card_name = detail[:-16].strip()
            red_names.append(red_card_name)

    print red_names
    


get_players(440409)
