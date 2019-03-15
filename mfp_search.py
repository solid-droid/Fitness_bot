from math import ceil
from bs4 import BeautifulSoup 
from urllib.request import urlopen
from urllib.request import Request
from fuzzywuzzy import fuzz

def calBurned(calCount=170,weight=70):
    #(calories/minute) = MET x weight (in kilograms)/60
    #MET w=3.5 c=5 r=8
    wTime = ceil(calCount*60/(3.5*weight))
    cTime = ceil(calCount*60/(5*weight))
    jTime = ceil(calCount*60/(8*weight))
    return [wTime,cTime,jTime]


def findFood(searchURL):
    surl = 'https://www.myfitnesspal.com/food/search?page=1&search='+ searchURL

    def getPage(url):
        ureq = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        return BeautifulSoup(urlopen(ureq).read(), 'lxml')

    def findItem():
        searchSoup = getPage(surl)
        flist = []
        mydivs = searchSoup.find_all("div", class_="food_info")
        for items in mydivs:
            flist.append((items.a.text,items.find("div", class_="nutritional_info").text))
        if flist == []:
            print("Error")

        maxRatio = 0
        maxItem = flist[0]
        for item in flist[::-1]:
            currentRatio=fuzz.ratio(searchURL.lower(),item[0].lower())
            if currentRatio >= maxRatio:
                maxRatio = currentRatio
                maxItem = item
        print("Search Term: " + searchURL + "\nClosest Match: " + maxItem[0])        
        return maxItem

        
    # Get Results
    foodItem = findItem()
    itemName = foodItem[0]
    itemNutrition = (' '.join(foodItem[1].split())).split(",")

# #========================================================Parse Output=============================================
   
    itemServ = itemNutrition[0][14:]
    itemCal = itemNutrition[1][11:]
    itemFat = itemNutrition[2][6:]
    itemCarb = itemNutrition[3][8:]
    itemProtein = itemNutrition[4][10:]
    

    print("Food Name: " + itemName)
    print("Calories: " + itemCal)
    print("Serving Size: " + itemServ)
    print("Carbs: " + itemCarb)
    print("Protein: " + itemProtein)
    print("Fat: " + itemFat)
    return [itemName,itemCal,itemCarb,itemFat,itemProtein,itemServ]
