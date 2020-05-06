import os
import plotly.graph_objects as go
import pandas
import random
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json


# basic statistic class
class Stat:
    index = 0
    date = ""
    newCases = 0

    def __init__(self, index, date, newCases):
        self.index = index
        self.date = date
        self.newCases = newCases

# returns the forecast based on the stats passed
def getForecast(Stats, count): 
    n = count - 1
    x_sum = 0
    y_sum = 0
    x_square = 0
    y_square = 0
    x_y = 0

    for stats in Stats:
        x_sum += stats.index
        y_sum += stats.newCases

        x_square += stats.index * stats.index
        y_square += stats.newCases * stats.newCases

        x_y += stats.index * stats.newCases

    a = ((x_square) * (y_sum) - (x_sum)*(x_y)) / ((n)*(x_square) - (x_sum)*(x_sum))

    b = ((n) * (x_y) - (x_sum)*(y_sum)) / ((n)*(x_square) - (x_sum)*(x_sum))

    regression = a + b * count

    return(regression)

# sumsCases
def sumCases(Stats):
    cases = 0
    for stat in Stats:
        cases += stat.newCases
    return(cases)

Stats = []
count = 0

# Loads stats from text file
with open("data.txt", "r") as filestream:
    for line in filestream:
        stats = line.split("*")
        stat_cases = stats[1].replace(',','')
        Stats.append(Stat(count ,stats[0], int(stat_cases)))
        count += 1

print("day {0} : cases {1}".format(count, getForecast(Stats, count)))
print()
print("quarantine")

numDays = 7

# will get the div elements that were returned! how neat is that
# tableCells = soup.findAll('table')[0].findAll('tr')

# print(tableCells)
dataGraphs = Stats.copy()

index = dataGraphs.count(0) - 1
quanartineData = []
quanartineData.append(dataGraphs[index])

# continues to forcast a week ahead of time, with current trends of staying home.
for x in range(numDays):
    forValue = getForecast(Stats, count)
    forValue = forValue * random.uniform(2.4, 2.9) * 0.2143
    print("{0} : {1}".format(count, forValue))
    Stats.append(Stat(count, "new date", int(forValue)))
    quanartineData.append(Stat(count, "new date", int(forValue)))
    count+=1

socialDistance = sumCases(Stats) + sumCases(quanartineData)

print("{0} total cases for 05/10/2020".format(socialDistance))
print()

for x in range(numDays):
    Stats.pop()
count += -numDays

print("non-quarantine")

nonQuarnData = []
nonQuarnData.append(dataGraphs[index])

for x in range(numDays):
    forValue = getForecast(Stats, count)
    forValue = forValue * random.uniform(2.4, 2.9) * 0.7857
    print("{0} : {1}".format(count, forValue))
    Stats.append(Stat(count, "new date", int(forValue)))
    nonQuarnData.append(Stat(count, "new date", int(forValue)))
    count+=1

for x in range(numDays):
    Stats.pop()
count += -numDays

noSociDistance = sumCases(Stats) + sumCases(nonQuarnData)
print("{0} total cases for 05/10/2020".format(noSociDistance))
newCases = noSociDistance - socialDistance

print("new cases = {0}, without quarantine".format(newCases))
print()
input("press any key to graph results")

index = 0
days = []
caseNon = []
caseSoc = []

for x in quanartineData:
    days.append(x.index)
    caseSoc.append(x.newCases)
    caseNon.append(nonQuarnData[index].newCases)
    index += 1

fig = go.Figure()
fig.add_trace(go.Scatter(x=days, y=caseSoc, name='Forcasting with social distancing',
                        line=dict(color='green', width=4)))
fig.add_trace(go.Scatter(x=days, y=caseNon, name='Forcasting without social distancing',
                        line=dict(color='firebrick', width=4)))

days = []
dataVal = []

for x in dataGraphs:
    days.append(x.index)
    dataVal.append(x.newCases)
# https://plotly.com/python/line-charts/
# adding multiple different lines to this polyLineChart

fig.add_trace(go.Scatter(x=days, y=dataVal, name='CDC daily case data',
                        line=dict(color='blue', width=4)))

fig.show()

# cases numbers 
# https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html
#
# https://www.psychologytoday.com/us/blog/laugh-cry-live/202004/the-shocking-numbers-behind-the-novel-coronavirus-pandemic
# reproduction of covid https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7074654/

