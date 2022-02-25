import threading
import fb
import json
import time
import requests
from bs4 import BeautifulSoup as bs

webhook = "https://discordapp.com/api/webhooks/646488319148163073/asoW2-tyA3JzAvdOgGRlE8hfnr0_p-AKZ0_PpyVhC9s1JRQtlAAeQWb7GYKsBbq_4VCv"

# bradburne (website)
# alba (fb)
# inchdairnie (email subscription)
# delmor (fb)
# premier let (email sub)
# braemore

with open('config.json') as data:
    data = json.load(data)
    
webhook = data['webhook']
delay = data['delay']
urlArray = data['urls']

def logger(module, message):
    print("{} - {}: {}".format(time.strftime("%H:%M:%S.{}".format(str(time.time() % 1)[2:])[:8], time.gmtime(time.time())), module, message))

    
def getPageSource(url):
    pageSource = bs(requests.get(url).text, "html.parser")
    
    return pageSource
    
def getRollosProperties():
    pageSource = getPageSource("https://www.rolloslettings.co.uk/letting-agents/lettings/")
    
    scriptTag = pageSource.find(id="propertyInitialState").text    
    trimmedEnds = scriptTag.replace("window.params = [];", "").rstrip().rstrip(";").replace("window.initial_property_state = ", "").lstrip()
    propertiesJson = json.loads(trimmedEnds)
    propertyList = []
    
    for property in propertiesJson['properties']:
        propertyList.append(property['property_post']['guid'])
    
    return propertyList


def postToDiscord(name, link):
    requests.post(webhook, json={
        "username": "New Property",
        "embeds": [
            {
                "color": "65535",
                "fields": [
                    {
                        "name": name,
                        "value": link
                    }
                ]
            }
        ]
    })
    

def getThortonsProperties():
    pageSource  = getPageSource("https://thorntons-lettings.co.uk/student-list/")
    
    table = pageSource.find("table", {"class": "data"}) 
    propertyList = []
    for row in table.findAll("a"):
        propertyList.append(row['href'])
        
    return propertyList
            
    
def getLawsonProperties():
    pageSource = getPageSource("https://www.lawsonthompson.co.uk/student-lettings/")
    
    allAvailableProperties = pageSource.find("div", {"class": "properties clear"})
    rawPropertyList = allAvailableProperties.findAll("div", {"class": "actions"})
    propertyList = []
    for property in rawPropertyList:
        propertyList.append(property.a['href'])
        
    return propertyList

def monitor(site):
    if site == "lawson":
        propertyList = getLawsonProperties()
    elif site == "rollos":
        propertyList = getRollosProperties()    
    elif site == "thorntons":
        propertyList = getThortonsProperties()
        
    while True:
        if site == "lawson":
            newList = getLawsonProperties()
        elif site == "rollos":
            newList = getRollosProperties()        
        elif site == "thorntons":
            newList = getThortonsProperties()
        
        if newList != propertyList:
            for property in newList:
                if property not in propertyList:
                    print("{} - NEW PROPERTY FOUND".format(site))
                    postToDiscord("New Property", property)
                    
            
            propertyList = newList
        else:
            logger(site, "No new properties")
        
        time.sleep(15)
    
    
# def fb():
#     pageSource = getPageSource("https://www.facebook.com/AlbaResidentialStAndrews/")
#     with open('readme.txt', 'w') as f:
#         f.write(str(pageSource))
    


if __name__ == "__main__":
    for url in urlArray:
        thread = threading.Thread(target=fb.run, args=[url])
        thread.start()
        time.sleep(delay/(len(urlArray)*1000))

    rollosThread = threading.Thread(target=monitor, args=["rollos"])
    thorntonsThread = threading.Thread(target=monitor, args=["thorntons"])
    
    thorntonsThread.start()
    rollosThread.start()    
    monitor("lawson")
    

        
    