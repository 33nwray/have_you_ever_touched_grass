# -*- coding: utf-8 -*-
"""
Created on Sat May 25 11:05:19 2024

@author: 33nwr
"""

import selenium
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import re
import time
import tqdm

#master_names = set()
#master_names_df = pd.DataFrame(master_names, columns=['Player'])
#master_names_df.to_csv('C:/Users/33nwr/OneDrive/Documents/Premier League Extraction/master_names.csv')

#master_names = set(pd.read_csv('C:/Users/33nwr/OneDrive/Documents/Premier League Extraction/master_names.csv')['Player'].tolist())

service = Service('C:/Users/33nwr/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe')    
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('prefs', {
    "download.default_directory": 'C:/Users/33nwr/OneDrive/Documents/Premier League Extraction', #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")


season_codes_06_to_15 = [#14, 15, 16, 17, 18, 19, 
                         20, 21, 22, 27]

driver = webdriver.Chrome(service=service, options = options)


for y, s in enumerate(season_codes_06_to_15):

    print('Year -' + str(y))
    driver.get(f"https://www.premierleague.com/players?se={s}&cl=-1")
    time.sleep(1)
    
    # if y == 0:
    #     #Close initial popups
    #     button = driver.find_element(By.XPATH, "//button[text()='Accept All Cookies']")
    #     button.click()
    #     time.sleep(1)
    #     button = driver.find_element(By.ID, 'advertClose')
    #     button.click()
    
    #Scroll to bottom of page to get all players
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(60)
    
    #Extract all player records
    players = driver.find_elements(By.CLASS_NAME, 'player')
    
    
    player = players[1]
    for num, player in enumerate(players):
        print('Iteration - ' + str(num))
        player_img = player.find_element(By.CLASS_NAME, 'player__name-image')
        player_img.get_attribute('outerHTML')
        
        if 'Photo-Missing' in player_img.get_attribute('src'):
            continue
        else:
            
            #player.text -> contains name, position, country -> to be used for  row
            
            #Get players' names
            name = player.find_element(By.TAG_NAME, 'a').text
            
            #Have they been processed before?
            if name in master_names:
                continue
            
            #Check if they made 100+ appearances
            #---
            #Load player
            e = player.find_element(By.CLASS_NAME, 'player__name')
            link = e.get_attribute("href")
            # Navigate to the extracted URL
            driver.get(link)
    
            time.sleep(1)
            #Get their stats
            layers = driver.find_elements(By.CLASS_NAME, 'player-overview__col')
    
            skip = False
            #l = layers[0]
            for i, l in enumerate(layers):
                #print('Layer - ' + str(i))
                
                try:
                    key = l.find_element(By.CLASS_NAME, 'player-overview__label').text
                    value = l.find_element(By.CLASS_NAME, 'player-overview__info').text
                
                    if key == 'Appearances':
                        if int(value) < 100:
                            skip = True
                except NoSuchElementException:
                    continue
                            
                #---
                #Room to store data here
                #
                #---
                        
            driver.back()
            time.sleep(1)
            
            #Move onto next player if less than 100 apps
            if skip == True:
                continue
            
            #Get image, load the bigger version and save
            img_link = re.sub('40x40', '250x250', player_img.get_attribute('src'))
            r = requests.get(img_link)
            path = f"C:/Users/33nwr/OneDrive/Documents/Premier League Extraction/{name}.png"
    
            with open(path, 'wb') as file:
                            file.write(r.content)
            
            master_names.add(name)


#master_names_df = pd.DataFrame(master_names, columns=['Player'])
#master_names_df.to_csv('C:/Users/33nwr/OneDrive/Documents/Premier League Extraction/master_names.csv')
