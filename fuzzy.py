from bs4 import BeautifulSoup 
from urllib.request import urlopen
from urllib.request import Request
from fuzzywuzzy import fuzz


# Search Parameters
 
pageNo='1'
searchURL='Iddli'

flist = []
# Search MFP
#url = 'https://www.myfitnesspal.com/food/search?page='+ pageNo + '&search='+ searchURL

searchSoup = BeautifulSoup(open("mfp.html",encoding="latin-1"), 'lxml')

mydivs = searchSoup.find_all("div", class_="food_info")
for items in mydivs:
    flist.append((items.a.text,items.a["href"]))

#print (flist)
maxRatio = 0

for item in flist:
    currentRatio=fuzz.ratio(searchURL.lower(),item[0].lower())
    if currentRatio > maxRatio:
        maxRatio = currentRatio
        maxItem = item
print("Search Term: " + searchURL)
print("Match%: " + str(maxRatio))
print("Name: " + maxItem[0] + "\nURL: " +maxItem[1])