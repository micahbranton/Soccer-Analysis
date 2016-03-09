from selenium import webdriver

driver = webdriver.Chrome()

match_id = []

for date in range(20130802,20130810):
	driver.get('http://www.espn.com.ar/futbol/resultados/_/liga/arg.1/fecha/' + str(date))

	match_link_driver = driver.find_elements_by_name('&lpos=soccer:scoreboard:resumen')

	match_links = []

	for i in range(len(match_link_driver)):
		match_links.append(match_link_driver[i].get_attribute('href'))

	for match in match_links:
		match_id.append(match[46:53])

	driver.quit

for i in match_id:
	print i