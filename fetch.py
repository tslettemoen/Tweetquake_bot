import requests
import json
from datetime import datetime

def gettime(address,parameters):
    #Fetches time of last earthquake according to parameters
    data = list()
    response = requests.get(address+parameters)
    for i in response:
        data.append(i)

    lastquake = str(data[1]).split("|")
    innittime = lastquake[1]
    innittime = innittime[:-4]
    return innittime

def getquakes(address,parameters,time):
    #Fetches list of earthquakes after set time, with chosen parameters
    #API returns GeoJSON format data. "Features" of earthquakes is then added
    #to list. Features are JSON
    quakes = list()
    print(address+parameters+time)
    response = requests.get(address+parameters+time)
    respjson = response.json()

    for i in respjson['features']:
        quakes.append(i)
    return quakes

def timecalcTOD(millitime):
    #Turns timestamp (unix time) to  ISO8601 time used in query.
    ts = int(millitime)/1000
    return(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S'))

def timecalc(millitime):
    #Turns timestamp (unix time) to  ISO8601 time used in query.
    ts = int(millitime)/1000
    return(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))

def getdatabaseitems(quakeout):
    #Extracts relevant data from JSON list given by "getquakes" function
    #outputs list of strings.
    outdata = list()
    for i in quakeout:
        print(i)
        for p in (i['properties']['mag'],
        i['geometry']['coordinates'],
        timecalc(i['properties']['time']),
        i['properties']['ids'],
        i['properties']['place']):
            outdata.append(p)
    return outdata
def QuakeReturn():
    #API address
    url = "https://earthquake.usgs.gov/fdsnws/event/1/"

    #Paramters for the "gettime" function
    textparam = "query?format=text&minmagnitude=4.0"

    #Parameters for the "getquakes" function
    jsonparam = "query?format=geojson&minmagnitude=4.0"

    #Parameter for "getquakes" function
    updateafter = "&starttime="
    updateafter += gettime(url,textparam)

    return(getdatabaseitems(getquakes(url,jsonparam,updateafter)))
