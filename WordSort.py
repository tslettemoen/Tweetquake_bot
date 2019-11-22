
#Creates a dict where words are key and number of times they occur
#is value.
def RankWords(ListToRank):
    WordDict = {}
    for i in ListToRank:
        Words = i.split()
        for x in Words:
            if x in WordDict:
                WordDict[x] += 1
            else:
                WordDict[x] = 1
    return WordDict

#Creates a list of top three occurring words from dict created by
#RankWords function
def GetTopThree(DictToRank):
    BaseLine = list(DictToRank.values())
    BaseLine.sort()
    TopThree = BaseLine[-3:]
    ReturnWords = []
    for x,y in DictToRank.items():
        if y in TopThree:
            ReturnWords.append(x)
    return ReturnWords
