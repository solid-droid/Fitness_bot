import re
from bs4 import BeautifulSoup 
from urllib.request import urlopen
from urllib.request import Request

# Search Parameters
 
pageNo='1'
searchURL='Pizza'
def findFood(searchURL):
    def getPage(url):
        ureq = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        return BeautifulSoup(urlopen(ureq).read(), 'lxml')


    # Search MFP
    url = 'https://www.myfitnesspal.com/food/search?page=1&search='+ searchURL
    searchSoup = getPage(url)
    item = searchSoup.find("div", class_="food_info")

    # Get Results
    url = 'https://www.myfitnesspal.com'+str(item.a["href"])
    soup = getPage(url)

    #========================================================Parse Output=============================================

    # Food Info
    itemName = soup.find("h3", class_="jss3 jss17 pageTitle-_5t9X").text
    itemName = itemName[itemName.find(' - ')+3:]
    itemCal = soup.find("h1", class_="title-cgZqW").text
    itemCarb = soup.find("h1", class_="carbohydrates-orw9p subtitle-7_FIi").text
    itemProtein = soup.find("h1", class_="protein-Eg08Q subtitle-7_FIi").text
    itemFat = soup.find("h1", class_="fat-lHyji subtitle-7_FIi").text

    print("Food Name: " + itemName)
    print("Calories: " + itemCal)
    print("Carbs: " + itemCarb)
    print("Protein: " + itemProtein)
    print("Fat: " + itemFat)

    # String Formatting for Exercise Info

    acString = soup.find("div",class_="inlineActivitiesContainer-2DZep").text
    repDict = {"Minutes": " Minutes", "Hours": " Hours","Seconds":" Seconds"}
    pattern = re.compile("|".join(repDict.keys()))
    acString = pattern.sub(lambda m: repDict[m.group(0)], acString)

    cyindex = acString.find('of Cycling')
    ruindex = acString.find('of Running')
    clindex = acString.find('of Cleaning')

    # Exercise Info

    timeCyc=acString[:cyindex]
    timeRun=acString[cyindex+10:ruindex]
    timeClean=acString[ruindex+10:clindex]

    print("Cycling: " + timeCyc)
    print("Running: " + timeRun)
    print("Cleaning: " + timeClean)
    return [itemName,itemCal,itemCarb,itemProtein,itemFat,timeCyc,timeRun,timeClean]

