from flask import *
import json
from zomato import *
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
    print(location)
    hotels, _=getTopRest(myWrapper,location )
    if(hotels==None):
        return("Sorry I could not find any results.")
    else:
        return ("Some of the top rated restaurants in the area are "+str(hotels[0])+", "+str(hotels[1])+" and "+str(hotels[2]))
##############################################################

def food():
    return(text)

###############################################################
def recipi():
    return(text)
###############################################################
def condition():
    return text

##################################################################


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
        text= food()

    if intent == "Recipi":
        text= recipi()

    if intent == "Diet":
        text= diet()


    # action = req.get('queryResult').get('action')
    # param = req.get('queryResult').get('parameter')

    print(text)
    return {'fulfillmentText': text}

@app.route('/assist', methods=['POST'])

def static_res():
    return make_response(jsonify(results()))
if __name__ == '__main__':
    print(hotel("Edappally"))
    app.run()