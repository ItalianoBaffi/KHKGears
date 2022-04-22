import csv
import datetime
import time
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
'''
# Grabs links for each path from main spur/helical gear page
for url in urls:
	driver.get(url)
	modules = driver.find_element(By.ID, 'cds-attribute-value-list-sort_module').find_elements(By.TAG_NAME,'input')
	# Selects every module
	for i in range(len(modules)):
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-sort_module')))
		hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-sort_module').find_elements(By.TAG_NAME,'input')[i]).perform()

		WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-no_teeth')))
		teeth = driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')
		for j in range(len(teeth)):
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-no_teeth')))
			hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')[j]).perform()

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
			hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')[j]).perform()
			print("Module: {}: {}%, Teeth: {}: {}%".format(i,100*i/len(modules),j,100*j/len(teeth))) # Shows Progress

		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-sort_module')))
		hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-sort_module').find_elements(By.TAG_NAME,'input')[i]).perform()
		'''
def grabParts(url, driver):
	global parts
	
	driver.get(url)
	hover = ActionChains(driver)
	modules = driver.find_element(By.ID, 'cds-attribute-value-list-sort_module').find_elements(By.TAG_NAME,'input')
	# Selects every module
	for i in range(len(modules)):
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-sort_module')))
		hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-sort_module').find_elements(By.TAG_NAME,'input')[i]).perform()

		WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-no_teeth')))
		teeth = driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')
		for j in range(len(teeth)):
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-no_teeth')))
			hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')[j]).perform()

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
			hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-no_teeth').find_elements(By.TAG_NAME,'input')[j]).perform()
			print("Module: {}: {}%, Teeth: {}: {}%".format(i,100*i/len(modules),j,100*j/len(teeth))) # Shows Progress

		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'cds-attribute-value-list-sort_module')))
		hover.click(driver.find_element(By.ID, 'cds-attribute-value-list-sort_module').find_elements(By.TAG_NAME,'input')[i]).perform()

# Gathers information from each part page and adds it to info list
def grabContent(part, driver):
	global info
	global parts

	driver.get(part)
	temp = []

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
	temp.append('<a href="'+part+'">'+driver.find_elements(By.CLASS_NAME,'productName')[0].get_attribute('textContent').spit('\n\t\t\t\t\t\t\t')[1]+'</a>',bending,surface,pitch,teeth,weight,bore,
			 driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[1],driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[2],
			 driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[3],driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[4],driver.find_elements(By.TAG_NAME,'tr')[1].find_elements(By.TAG_NAME,'td')[5])

	# Adds list of information to main info list
	info.append(temp)

	print("Progress {}%".format(100*len(info)/len(parts))) # Shows Progress


if __name__ == "__main__":
	# Handles multithreading of pulling information
	drivers = [webdriver.Chrome(options=options) for _ in range(len(urls))]
	prt = cf.ThreadPoolExecutor()
	prt.map(grabParts,urls,drivers)

	[driver.quit() for driver in drivers]

	drivers = [webdriver.Chrome(options=options) for _ in range(len(parts))]
	ex = cf.ThreadPoolExecutor()
	ex.map(grabContent,parts,drivers)

	[driver.quit() for driver in drivers]

	# Creates and writes information to file
	with open('./outputFiles/kgkGearsOutput '+datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")+'.csv','w+') as file:
		file = csv.writer(file)
		file.writerows(info)
	print("Complete!")
