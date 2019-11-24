import sys
import fetch #To get earthquake info
import twittersearch #To search and post to twitter
import sqlite3 #Module to connect and manipulate SQLite database
import WordSort #To format words correctly for tweet
import time #Module used to sleep the system, so that the API limitations
            #are not invoked

#connects to database "Quakes.db"
connection = sqlite3.connect("Quakes.db")
curs = connection.cursor()

#fetches data from latest earthquake by parameters defined in "fetch"
data = fetch.QuakeReturn()
print(data)

#Overarching loop to search for tweets multiple times for one earthquake
while True:

    #Fetches tweets based on earthquake data
    Tweets = twittersearch.SearchTweets(data)
    TweetText = []

    #Loops through all individual statuses. Discards all extra info
    for i in Tweets["statuses"]:
        ListToDatabase = []
        print(int(i['id']))
        SplitWords = str(i['text']).split()
        for x in SplitWords:

            #Only saves words of 3 characters or more, excluding the word
            #earthquake. Adds these words to list being sent to database
            if len(x) > 3 and not "QUAKE" in x.upper():
                ListToDatabase.append(x)
            else:
                continue

        #SQL command for writing the collected words, along with the ID of the
        #tweet for later reference
        curs.execute("""INSERT INTO Tweets (ID,Text) VALUES (?,?)""",
        (int(i['id']),str(ListToDatabase)))

    #Writes changes to the database, so that the info can be accessed
    #at a later point in the run.
    connection.commit()

    #Command to select all words written to database
    command = """SELECT Text FROM Tweets"""

    #This executes the command above
    result = curs.execute(command)

    #Empty list to store words from database
    WordsFromDatabase = []

    #Loops through data from database. Multiple loops nested to format data
    #correctly
    for i in result:
        for x in i:
            for y in x.split(',", "'):
                for z in y[1:-1].split(', '):
                    WordsFromDatabase.append(z[1:-1])

    #Calls functions to first rank the words by occurrence and get the top
    #three words, which will be included in the tweet
    print(WordsFromDatabase)
    DictWords = WordSort.RankWords(WordsFromDatabase)
    print(DictWords)
    TopThreeWords = WordSort.GetTopThree(DictWords)
    print(TopThreeWords)

    #Try block in case there are no elligible tweets gathered. If there are the
    #program will end and a tweet will be posted, if not the program tries to
    #search again in 15 minutes.
    try:
        print(twittersearch.PostTweet(data[0],data[-1],TopThreeWords))
        sys.exit()
    except:
        time.sleep(900)
        continue
