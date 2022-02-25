from hashlib import new
import json
import threading
import requests
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('config.json') as data:
    data = json.load(data)
    
webhook = data['webhook']
delay = data['delay']
urlArray = data['urls']


def getNextUrl(currentUrl):
    newIndex = urlArray.index(currentUrl) + 1
    if newIndex == len(urlArray):
        newIndex = 0
    
    return urlArray[newIndex]
    
def run(url):
    
    print("Using Home IP")
    
    
    browser = webdriver.Chrome("../drivers/chromedriver")

    browser.get(url)

    #time.sleep(50000)
    # CODE TO DISMISS COOKIES BUTTON
    clearCookiesButton = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Allow Essential and Optional Cookies')]")))
    clearCookiesButton.click()
    
    # browser.maximize_window()

    # clearCookiesActions = ActionChains(browser)
    # clearCookiesActions.send_keys(Keys.TAB*7 + Keys.ENTER)
    # clearCookiesActions.perform()
        
    # browser.execute_script("window.scrollTo(0, 500)")
    
    # seeMoreButton = WebDriverWait(browser, 5).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'See more')]")))
    # seeMoreButton.click()
    
    # messageBox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ad-preview="message"')))
    mostRecentMessageContent = None
    
    while True:
        try:
            clearCookiesButton = WebDriverWait(browser, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Allow Essential and Optional Cookies')]")))
            clearCookiesButton.click()
        except Exception:
            pass
    
        newMessageBox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ad-preview="message"')))
        browser.execute_script("window.scrollTo(0, 500)")

        seeMoreButton = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'See more')]")))
        seeMoreButton.click()
        
        newMessageBox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ad-preview="message"')))
        newMostRecentMessageContent = newMessageBox.text
        
        
        if (newMostRecentMessageContent != mostRecentMessageContent) and (mostRecentMessageContent != None) :
            print("&&&&&&&&&&& NEW ALBA POST &&&&&&&&&&&")
            
            mostRecentMessageContent = newMostRecentMessageContent
            
            # discordContent = ' '.join(mostRecentMessageContent.split())
            # print(discordContent)
            requests.post(webhook, json={
                "username" : "New Alba Property",
                "embeds": [{
                    "title": "Alba Facebook Page",
                    "url": "https://www.facebook.com/AlbaResidentialStAndrews",
                    "color": 8341306,
                    "fields": [
                    {
                        "name": "Description",
                        "value": mostRecentMessageContent[:1024]
                    }
                    ]
                }]
            })
            
        else:
            print("no new posts found. retrying... --------------------------------")
            
        time.sleep(delay/1000)
        browser.refresh()

if __name__ == "__main__":
    for url in urlArray:
        thread = threading.Thread(target=run, args=[url])
        thread.start()
        time.sleep(delay/(len(urlArray)*1000))