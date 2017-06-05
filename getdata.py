import requests
import re
from bs4 import BeautifulSoup

#setup
basicHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
ExtraHeader = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
'Referer': 'https://disneyworld.disney.go.com/dining/magic-kingdom/be-our-guest-restaurant/',
'Host': 'disneyworld.disney.go.com', 
'Origin': 'https://disneyworld.disney.go.com',
'Connection':'keep-alive',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'en-US,en;q=0.8',
'X-Requested-With':'XMLHttpRequest',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Accept':'*/*'
}

InitURL = "https://disneyworld.disney.go.com/dining/magic-kingdom/be-our-guest-restaurant/"
RequestURL = "https://disneyworld.disney.go.com/finder/dining-availability/"
session = ""
pep = ""

def startSession():
    global session
    global pep
    session = requests.Session()
    session.headers.update(basicHeader)
    #Get PEP
    tokenRequest = session.get(InitURL)
    match = re.search('"[a-z0-9]{128}"', tokenRequest.text)
    pep = match.group(0)[1:-1] 

def getByTime(inputTime, inputDate, inputParty):
    payload = {
    'pep_csrf': pep,
    'searchDate': inputDate,
    'skipPricing': "true",
    'searchTime': inputTime,
    'partySize': inputParty,
    'id': "16660079;entityType=restaurant",
    'type': "dining"
    }
    result = session.post(RequestURL, headers=ExtraHeader, data=payload)
    soup = BeautifulSoup(result.text, "html.parser")
    times = soup.find_all("div", {"class", "availableTime"})
    FullResponse = []
    if times.count == 0:
        return FullResponse
    for time in times:
        FullResponse.append(time.get_text().strip())
    return FullResponse

def getByDate(inputDate, inputParty):
    searchTimes = ["80000712", "80000717", "80000714"]
    FullResponse = [getByTime(searchTimes[0], inputDate, inputParty), getByTime(searchTimes[1], inputDate, inputParty), getByTime(searchTimes[2], inputDate, inputParty)]
    print(FullResponse)
    return FullResponse