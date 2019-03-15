from flask import *
import json
from zomato import *
from mfp import*
myWrapper=ZomatoWrapper(API_KEY)

text="none"
req=""

def exercise():
    return(text)

#########################################################
def diet():

    return(text)
# #######################################################
def hotel(strng):
    strng=strng.split()
    location=strng[-1]
    location=location.capitalize()
    if(location=="Restaurants" or location=="Restaurant" or location=="Hotel" or location=="Hotels"):
        return ("Sorry no location was specified.")
    hotels, _=getTopRest(myWrapper,location )
    if(hotels==None):
        return("Sorry I could not find any results.")
    else:
        return ("Some of the top rated restaurants in the area are "+str(hotels[0])+", "+str(hotels[1])+" and "+str(hotels[2]))
##############################################################

def food(val,cal):
    val=val.title()
    dat = findFood(str(val))
    cal=int(cal)/3
    if int(dat[1]) < cal:
        return "The " + str(dat[0]) + " consist of " + str(dat[1]) + " Calories a serving, which goes fine with your diet plan"
    else:
        return "The " + str(dat[0]) + " consist of " + str(dat[1]) + " Calories a serving, you must restrict your food intake to follow your diet plan"


###############################################################
def recipi():
    return(text)
###############################################################
def condition():
    return text

##################################################################
def calo(val,typ):
    val = val.title()
    print(val)
    dat = findFood(str(val))
    if(typ=="calories"):
        return str(dat[0]) + " contains " + str(dat[1]) +" calories"
    if(typ=="carb"):
        return str(dat[0]) + " contains " + str(dat[2]) +" carbs"
    if(typ=="fat"):
        return str(dat[0]) + " contains " + str(dat[3]) +" fat"
    if(typ=="protein"):
        return str(dat[0]) + " contains " + str(dat[4]) +" protein"
###############################################################
app = Flask(__name__)
def results():
    text="none"
    req = request.get_json(force=True)
    print(req)
    intent = req.get('queryResult').get('intent').get('displayName')
    print(intent)
    if intent == "Exercise" :
        text= exercise()

    if intent == "Restaurant":
        text= hotel(req.get('queryResult').get('queryText'))

    if intent == "Food":
        num=req.get('queryResult').get('parameters').get('number')
        fd=req.get('queryResult').get('parameters').get('food')
        text= food(fd,num)

    if intent == "Recipi":
        text= recipi()

    if intent == "Diet":
        text= diet()

    if intent == "calorie":
        num = req.get('queryResult').get('parameters').get('Burn')
        fd = req.get('queryResult').get('parameters').get('food')
        text= calo(fd,num)

    # action = req.get('queryResult').get('action')
    # param = req.get('queryResult').get('parameter')

    print(text)
    return {'fulfillmentText': text}

@app.route('/assist', methods=['POST'])

def static_res():
    return make_response(jsonify(results()))
if __name__ == '__main__':
    app.run()