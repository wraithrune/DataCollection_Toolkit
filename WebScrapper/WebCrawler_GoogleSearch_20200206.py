# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 21:58:26 2020

@author: HO Wei Jing

Website: wraithrune.myportfolio.com

"""
# Setup Libraries
import csv
import random
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Setup Variables
vSearchString = "Knowledge Engineering" # Input Keywords for the Search
vEntryNO = 0 # Starting Entry of Search Query is Set @ 0 for 1st Entry 
vCoreDictionary_SearchEntries = {} #Title (vTitle), Breadcrumbs (vBreadcrumbs), Link (vURL), Summary (vSummary), Raw Timestamp (vRawTimeStamp), Human Readable Timestamp (vTimestamp)
vTitle = ""
vBreadcrumbs = ""
vURL = ""
vSummary = ""
vRawTimeStamp = 0.0
vTimestamp = ""

# Setup Functions
def fUpdateSearchPath(vSearchString, vPageNO):
    # Setup the Google Search Query, Starting from Page X
    vSearchPath = "https://www.google.com/search?q=" + vSearchString + "&start=" + str(vEntryNO)
    return vSearchPath

def fRandomPause(vStartNo, vEndNo, vStep):
    vRandomNo = random.randrange(vStartNo, vEndNo, vStep)
    time.sleep(vRandomNo) # Random Sleep
    vReturnString = "Pause for " + str(vRandomNo) + " counts."
    print(vReturnString)
    return vReturnString

# Step 1 - Setup Chrome Driver
driver = webdriver.Chrome('F:/4_CodeExperiments_Python_R/0_CrawlerEXE/chromedriver.exe')

# Step 2 - WHILE Page is not the End > GET All Search Items from the Pages 
#          > UPDATE CSV > Then PROCEED to Next Page (ITERATE)

# Step 2 - Start Google Search Query
while vEntryNO <200:
    # Step 2A - Set Pause
    # Etiquette: Don't Scrap too Fast
    fRandomPause(2, 5, 1)
    
    # Step 2B - Update Search Page
    try:
        driver.get(fUpdateSearchPath(vSearchString, vEntryNO));
    
        # Step 2C - Get the Following Items:
        # >>> Title (vTitle), Breadcrumbs (vBreadcrumbs), Link (vURL), Summary (vSummary)
        
        # Step 2C(i) - Parse the Search Items for Each Page into Beautiful Soup (vBS4)
        # Current Assumption (dated: 26/01/2020) The Search Items are divided into two classes (r) and (s)
        # >>> (r) contains the Breadcrumbs, Title, Link
        # >>> >>> the subclass in (r) containing Title text is (LC20lb)
        # >>> (s) contains the Summary
        fRandomPause(2, 4, 1) # Pause
        
        vFindElementByClass_ForTitle = driver.find_elements_by_class_name('LC20lb')
        vFindElementByClass_ForBreadcrumbsAndURL = driver.find_elements_by_class_name('r')
        vFindElementByClass_ForSummary = driver.find_elements_by_class_name('s')
        
        for i in range(len(vFindElementByClass_ForBreadcrumbsAndURL)):
            vBS4 = BeautifulSoup(vFindElementByClass_ForBreadcrumbsAndURL[i].get_attribute('innerHTML'))
            
            # Step 2C(ii) - Retrieve All Web Links within Search Item
            # Current Assumption (dated: 26/01/2020) the First Web Link is the Link for the Search Item
            vRawURLChunk = vBS4.find_all('a')
            
            vTempURLArray = []
            for vTempURL in vRawURLChunk:
                vTempURLArray.append(vTempURL)
            
            vURL = vTempURLArray[0].get('href')
            
            # Step 2C(iii) - Retrieve the Breadcrumbs for the Search Item
            # Current Assumption (dated: 26/01/2020) Breadcrumbs are Associated with Text in the First Web Link
            vBreadcrumbs = vTempURLArray[0].text
            
            # Step 2C(iv) - Retrieve the Title for the Search Item
            vTitle = vFindElementByClass_ForTitle[i].text
            
            # Step 2C(v) - Retrieve the Summary for the Search Item
            vSummary = vFindElementByClass_ForSummary[i].text
            
            # Step 2C(vi) - Include Timestamp Data
            vRawTimeStamp = time.time()
            vTimestamp = str(time.ctime(vRawTimeStamp))
            
            # Step 2C(vii) - Print Statements for Each Entries
            print("Entry: ", str(i + vEntryNO))
            print("vTitle: ", vTitle)
            print("vBreadcrumbs: ", vBreadcrumbs)
            print("vURL: ", vURL)
            print("vSummary: ", vSummary)
            print("vRawTimeStamp: ", vRawTimeStamp)
            print("vTimeStamp: ", vTimestamp)
            
            # Step 2C(viii) - Append All Parameters into a Temp Array (vTemp_AllArray) 
            vTemp_AllArray = []
            
            vTemp_AllArray.append(str(i + vEntryNO))
            vTemp_AllArray.append(vTitle)
            vTemp_AllArray.append(vBreadcrumbs)
            vTemp_AllArray.append(vURL)
            vTemp_AllArray.append(vSummary)
            vTemp_AllArray.append(vRawTimeStamp)
            vTemp_AllArray.append(vTimestamp)
            
            # Step 2C(ix) - Add into Dictionary - Use Point of Entry as Key in Case Google Rank
            # >>> Search Items by Relevancy
            # >>> Only Add Those with Full Details
            if len(vTitle) != 0:
                vCoreDictionary_SearchEntries[str(i + vEntryNO)] = vTemp_AllArray
            
        
        # Step 2D - Save current extracted info to date + Flip to next search page     
        # Current Assumption (dated: 26/01/2020) Each query page contains 10 search entries
        
        # Step 2D(i) - Save the current extracted info to date
        vTemp_DataFrame = pd.DataFrame.from_dict(vCoreDictionary_SearchEntries, orient="index", columns=['Entry NO.', 'Title', 'Breadcrumbs', 'Link', 'Summary', 'Raw Timestamp', 'Readable Timestamp'])
        vTemp_DataFrame.to_csv("GoogleSearch_20200126_"+ vSearchString +".csv")    
            
        # Step 2D(ii) - + 10 to proceed to next search page
        vEntryNO = vEntryNO + 10
    except:
        print("No more pages")

# Step 3 - Close Browser Automation
fRandomPause(1, 5, 1) # Pause
driver.quit()