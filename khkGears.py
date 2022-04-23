import csv
import datetime
import concurrent.futures as cf
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Initializes lists to be used
urls = ['https://www.khkgears.us/catalog/?cid=spur-gears','https://www.khkgears.us/catalog/?c=fsearch&cid=helical-gears']
parts = []
info = [['Name','Bending Strength (N-m)','Surface Strength (N-m)','Pitch Diameter (mm)','Teeth','Weight (kg)','Bore (mm)','Price (1-9)','Price (10-24)','Price (25-49)','Price (50-99)','Price (100-249)']]
options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def grabParts(url, i, driver, teeth):
	global parts
	global urls
	
	driver.get(url)
	hover = ActionChains(driver)
	
	# Selects every tooth
	WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-no_teeth')))
	hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')[i]).perform()

	WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, 'cds-attribute-value-list-no_teeth')))
	# Ensures every part is displayed on the list
	try:
		WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME,'loadmore-link')))
		while len(driver.find_elements(By.CLASS_NAME,'loadmore-link')) != 0:
			hover.click(driver.find_elements(By.CLASS_NAME,'loadmore-link btn btn-default')[0]).perform()
			try:
				WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME,'loadmore-link')))
			except:
				pass
	except:
		pass

	# Grabs and adds link to parts list
	for partName in driver.find_elements(By.TAG_NAME,'h2'):
		parts.append(partName.find_elements(By.TAG_NAME,'a')[0].get_attribute('href'))

	WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-no_teeth')))
	hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')[i]).perform()
	print("Url {} Tooth Progress: {:.2f}%".format(urls.index(url)+1,100*(i+1)/teeth)) # Shows Progress

# Gathers information from each part page and adds it to info list
def grabContent(part, driver):
	global info
	global parts

	driver.get(part)

	# Searches for relevant data in list and assigns value to variable
	for label in driver.find_elements(By.CLASS_NAME,'label'):
		content = label.get_attribute('textContent')
		if content == 'Bending Strength (N-m)':
			bending = label.find_element(By.XPATH,'//following-sibling::div').get_attribute('textContent')
		elif content == 'Surface Durability (N-m)':
			surface = label.find_element(By.XPATH,'//following-sibling::div').get_attribute('textContent')
		elif content == 'Pitch Diameter (C)':
			pitch = label.find_element(By.XPATH,'//following-sibling::div').get_attribute('textContent')
		elif content == 'No. of teeth':
			teeth = label.find_element(By.XPATH,'//following-sibling::div').get_attribute('textContent')
		elif content == 'Weight':
			weight = label.find_element(By.XPATH,'//following-sibling::div').get_attribute('textContent')
		elif content == 'Bore (A)':
			bore = label.find_element(By.XPATH,'//following-sibling::div').get_attribute('textContent')

	# Creates a list of all the information pulled
	temp = ['<a href="'+part+'">'+driver.find_elements(By.CLASS_NAME,'productName')[0].get_attribute('textContent').split('\n\t\t\t\t\t\t\t')[1]+'</a>',bending,surface,pitch,teeth,weight,bore,
			 driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[1],driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[2],
			 driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[3],driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[4],driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[5]]

	# Adds list of information to main info list
	info.append(temp)

	print("Content Progress {:.2f}%".format(100*len(info)/len(parts))) # Shows Progress


if __name__ == "__main__":
	print("Starting...")
	# Handles multithreading based on tooth count
	for url in urls:
		tempDriver = webdriver.Chrome(options=options)
		tempDriver.get(url)
		teeth = len(tempDriver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input'))
		drivers = [webdriver.Chrome(options=options) for _ in range(teeth)]
		with cf.ThreadPoolExecutor() as prt:
			prt.map(grabParts,[url for _ in range(teeth)],list(range(teeth)),drivers,[teeth for _ in range(teeth)])
	
	print("Url fetching complete!")

	# Handles multithreading for data fetching
	drivers = [webdriver.Chrome(options=options) for _ in range(len(parts))]
	with cf.ThreadPoolExecutor() as ex:
		ex.map(grabContent,parts,drivers)

	tempDriver.quit()
	[driver.quit() for driver in drivers]
	print("Data fetching complete!")

	# Creates and writes information to file
	with open('./outputFiles/kgkGearsOutput '+datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")+'.csv','w+') as file:
		file = csv.writer(file)
		file.writerows(info)
	print("Complete!")
