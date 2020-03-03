import requests
from requests_oauthlib import OAuth1
import json

#URL and OAuth authentication used in requests. Mainly get requests
#Need to build function to get them from file, but for now it is easier
#to hardcode.
ApiUrl = 'https://api.twitter.com/1.1/search/tweets.json?q=earthquake'
hand = open("keystokens.txt")
credns = []
for i in hand:
    credns.append(i.rstrip())
Auth = OAuth1(tuple(credns))
hand.close()

#Function that searches for tweets based on earthquake data. This takes a list
#and fills it into the parameters sent as a get request to Twitter, but a dictionary would be
#better.
def SearchTweets(QuakeData):

    Coordinates = str(QuakeData[1][0])+','+str(QuakeData[1][1])+','+str(int(QuakeData[1][2])*10)+'km'
    Time = QuakeData[2]
    Params = '%20since%3A'+Time+'&result_type=recent'
    Url = ApiUrl+Params
    Resp = requests.get(Url, auth=Auth)
    return(Resp.json())
    #'&geocode='+Coordinates+

#Function to send a post request to Twitter. Takes three strings as arguments.
#Formats these into request. Printing tweet might not be necessary, but still
#useful sometimes.
def PostTweet(Magnitude,Location,ListToTweet):
    Tweet = "Earthquake of magnitude {} found in: \' {} \'. Described as \'{}\', \'{}\', \'{}\'".format(Magnitude,
    Location,ListToTweet[0],ListToTweet[1],ListToTweet[2])
    print(Tweet)
    status = requests.post("https://api.twitter.com/1.1/statuses/update.json", data=Tweet, auth=Auth)
    return status
