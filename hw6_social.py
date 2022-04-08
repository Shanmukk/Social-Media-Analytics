"""
Social Media Analytics Project
Name:
Roll Number:
"""

from fileinput import filename
from tkinter import CENTER
import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
from collections import Counter
import operator
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    d = pd.read_csv(filename)
    df = pd.DataFrame(d)
    return df


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    s1 = fromString.find(":") + 1
    s2 = fromString.find("(")
    s = fromString[s1:s2]
    s = s.strip()
    return s


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    s1 = fromString.find("(") + 1
    s2 = fromString.find(" from")
    s = fromString[s1:s2]
    return s


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    s1 = fromString.find("from") + len("from")
    s2 = fromString.find(")")
    s = fromString[s1:s2]
    s = s.strip()
    return s


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    line = message.split("#")
    s = []
    v = ""
    for i in range(1,len(line)):
        for j in line[i]:
            if j in endChars:
                break
            else:
                v += j
        v = "#" + v
        s.append(v)
        v = ""
    return s 


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    s = stateDf.loc[stateDf['state'] == state, 'region']
    return s.values[0]


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    name = []
    position = []
    state = []
    region = []
    hashtags = []
    for index,row in data.iterrows():
        s = row["label"]
        name.append(parseName(s))
        position.append(parsePosition(s))
        state.append(parseState(s))
        region.append(getRegionFromState(stateDf, parseState(s)))
        n = row["text"]
        hashtags.append(findHashtags(n))
    data["name"] = name
    data["position"] = position
    data["state"] = state
    data["region"] = region
    data["hashtags"] = hashtags
    return 


### PART 2 ###
'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score < -0.1:
        return "negative"
    elif score > 0.1:
        return "positive"
    else:
        return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentiment = []
    for index,row in data.iterrows():
        s = row["text"]
        sentiment.append(findSentiment(classifier, s))
    data["sentiment"] = sentiment
    return


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    s = {}
    for index,row in data.iterrows():
        #print(colName)
        if len(colName) != 0 and len(dataToCount) != 0:
            #print(row[colName])
            #print(dataToCount)
            if row[colName] == dataToCount:
                if row["state"] in s:
                    s[row["state"]] += 1
                else:
                    s[row["state"]] = 1
        else:
            if row["state"] in s:
                s[row["state"]] += 1
            else:
                s[row["state"]] = 1
    #print(s)
    return s

'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    d = {}
    for index,row in data.iterrows():
        if row['region'] not in d:
            d[row['region']] = {}
        if row[colName] in d[row['region']]:
            d[row['region']][row[colName]] += 1
        else:
            d[row['region']][row[colName]] = 1
    return d


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    tag_dict = {}
    for index,row in data.iterrows():
        tags = row["hashtags"]
        for i in range(len(tags)):
            if tags[i] not in tag_dict:
                #print(tags[i])
                tag_dict[tags[i]] = 1
            else:
                tag_dict[tags[i]] +=1
    #print(len(tag_dict))
    return tag_dict


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    most_common = {}
    s = Counter(hashtags)
    n = count
    sort = list(sorted(s.items(), key=operator.itemgetter(1),reverse=True))[:n]
    for key,value in sort:
        most_common[key] = value
    return most_common

'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    v = []
    for index,row in data.iterrows():
        f = row['text']
        if hashtag in f:
            s = row["sentiment"]
            if s == "positive":
                v.append(1)
            elif s == "negative":
                v.append(-1)
            elif s == "neutral":
                v.append(0)
    avg = sum(v)/len(v)
    return avg


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    lst = list(stateCounts.items())
    for key,value in lst:
        labels = key
        yValues = value
        plt.bar(labels,yValues,color='red')
        plt.xlabel(title,loc='center')
        plt.xticks(rotation="vertical")
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    feature ={}
    h = {}
    for i in stateFeatureCounts:
        feature[i] = stateFeatureCounts[i]/stateCounts[i]
    s = Counter(feature)
    sort = list(sorted(s.items(), key=operator.itemgetter(1),reverse=True))[:n]
    for key,value in sort:
        h[key] = value
    graphStateCounts(h,'top n state')
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    region_names = []
    feature_names = []
    region_feature = []
    for key,values in regionDicts.items():
        feature_names.append(key)
        temp = []
        for region,feature in values.items():
            if region not in region_names:
                region_names.append(region)
            temp.append(feature)
        region_feature.append(temp)
    sideBySideBarPlots(region_names,feature_names,region_feature,title)
    return

'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    hash_tags = []
    frequency = []
    sentiment = []
    hashtag = getHashtagRates(data)
    top = mostCommonHashtags(hashtag,50)
    for key,value in top.items():
        hash_tags.append(key)
        frequency.append(value)
        sentiment.append(getHashtagSentiment(data,key))
    scatterPlot(frequency,sentiment,hash_tags,"sentiment graph")
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    '''print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()'''

    ## Uncomment these for Week 2 ##
    '''print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()'''

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
    '''test.testMakeDataFrame()
    test.testParseName()
    test.testParsePosition()
    test.testParseState()
    test.testFindHashtags()
    test.testGetRegionFromState()
    test.testAddColumns()
    test.testFindSentiment()
    test.testAddSentimentColumn()
    df = makeDataFrame("data/politicaldata.csv")
    stateDf = makeDataFrame("data/statemappings.csv")
    addColumns(df, stateDf)
    addSentimentColumn(df)
    #df.to_csv("C:\\Users\\HP\\OneDrive\\Desktop\\Book1.csv")
    test.testGetDataCountByState(df)
    test.testGetDataForRegion(df)
    test.testGetHashtagRates(df)
    test.testMostCommonHashtags(df)
    test.testGetHashtagSentiment(df)'''
    
