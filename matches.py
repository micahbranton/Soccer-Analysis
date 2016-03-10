from selenium import webdriver
from datetime import date, timedelta

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