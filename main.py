#!/usr/bin/env python
# coding: utf-8

# In[22]:



import os
import numpy as np
import selenium
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException,InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import pygsheets
import pandas as pd
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

#chrome_options.headless = True # also works

driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

#driver = webdriver.Chrome(r"C:\Users\SteelSeries\Desktop\Chromedriver.exe")

driver.implicitly_wait(4)


# In[25]:


def selex(idx, x,wks):
    global driver
    driver.get(x)
    sleep(1)

    try :
        driver.find_element_by_xpath('//*[@id="react-root"]/div/div/p')

    except NoSuchElementException :
        try:
            stat = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/header/div/h1').text
            print(stat)
        except NoSuchElementException :
            stat = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/header/div[1]/h1').text
            print(idx)

        wks.update_value('C' + str(idx +2) ,stat)

        try :
            dtls = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/header/div/p').text
        except NoSuchElementException :
            dtls = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/header/div/p').text
        wks.update_value('E' + str(idx +2) ,dtls)

        try :


            img = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[1]/img').get_attribute('src')
            wks.update_value('F' + str(idx +2) ,img)
        except NoSuchElementException:
            pass





#wks.update_value('C' + str(idx +2) ,stat)


#authorization
#Obtained freely from googlesheetapi
gc = pygsheets.authorize(service_file='my-project-1515950162194-4db978de441c.json')


# In[ ]:


interval = 60 #seconds
iterations = 10 #times


# In[31]:
def runner():
    while (iterations > 0):
        sh = gc.open('Monitoro Tracker')
        #select the first sheet
        wks = sh[0]
        rt = pd.DataFrame(wks.get_all_records())
        ft = rt.copy()
        ft = ft.reset_index().rename(columns = {'index':'indexz'})

        ft.apply(lambda x : selex(x.indexz,x['Order URL'],wks), axis=1)
        sleep(interval)
    # In[ ]:
if __name__ == '__main__' :
    runner()
