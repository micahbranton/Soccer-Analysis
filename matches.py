from selenium import webdriver
from datetime import date, timedelta

driver = webdriver.Chrome()

def date_range(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield (start_date + timedelta(n)).strftime('%Y%m%d')

match_id = []
dates = []

for x in date_range(date(2016, 2, 5), date(2016, 2, 15)):
    dates.append(x)

for date in dates:
	driver.get('http://www.espn.com.ar/futbol/resultados/_/liga/arg.1/fecha/' + date)

	match_link_driver = driver.find_elements_by_name('&lpos=soccer:scoreboard:resumen')

	match_links = []

	for i in range(len(match_link_driver)):
		match_links.append(match_link_driver[i].get_attribute('href'))

	for match in match_links:
		match_id.append(match[46:53])

	driver.quit

for i in match_id:
	print i