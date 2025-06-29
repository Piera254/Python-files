#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
from datetime import datetime
import os
import sys

application_path = os.path.dirname(sys.executable)
website = "https://www.thesun.co.uk/sport/football/"
now = datetime.now()
#mmddyy
month_day_year = now.strftime("%m%d%y") #check strftime cheatsheet

options = Options()
options.headless = True
service = Service(EdgeChromiumDriverManager(version="135.0.3179.66").install())
driver = webdriver.Edge(service=service, options=options)

driver.get(website)

# Wait for teaser items to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "teaser-item")]'))
    )
except:
    print("Elements did not load.")
    driver.quit()
    exit()

# Get containers
containers = driver.find_elements(By.XPATH, '//div[contains(@class, "teaser-item")]')
print(f"Found {len(containers)} containers.")

titles = []
subtitles = []
links = []

for container in containers:
    try:
        title = container.find_element(By.XPATH, './div/a/span').text
        subtitle = container.find_element(By.XPATH, './div/a/h3').text
        link = container.find_element(By.XPATH, './div/a').get_attribute("href")
        titles.append(title)
        subtitles.append(subtitle)
        links.append(link)
    except:
        pass  # Skip if element is missing

# Save to CSV
my_dict = {'title': titles, 'subtitle': subtitles, 'link': links}
df = pd.DataFrame(my_dict)

file_name = f'headline{month_day_year}.csv'
final_path = os.path.join(application_path, file_name)

df.to_csv(final_path, index=False)

driver.quit()

