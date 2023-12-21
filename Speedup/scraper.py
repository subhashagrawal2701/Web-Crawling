import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random
import sys
import os

#HELPER FUNCTION TO TO CONVERT LIST TO STRINGS
def listToString(s):

	# initialize an empty string
	str1 = ""

	# traverse in the string
	for ele in s:
		str1 += ele

	# return string
	return str1

# To Connect to Database
def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return con, cur

# To fetch data from the given URL - to get Wikepedia using headers
def getData(url):        
    # Set a User-Agent header to identify your request
    headers = {
        "User-Agent": "My Wikipedia Scraper"
    }

    # Send a GET request with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the content of the page
        return response.content
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

#gives an url of row whose done is 0, and makes its done=1 
def giveurl(dbName):
    con, cursor = createDatabaseConnect(dbName)
    query = "SELECT * FROM SummerOlympics WHERE DONE_OR_NOT_DONE = 0 AND Name IS NULL LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
         cursor.close()
         con.close()
         return None
    else:
         iurl=result[1]
         query = "UPDATE SummerOlympics SET DONE_OR_NOT_DONE = 1 WHERE WikipediaURL = ?"
         cursor.execute(query, (iurl,))
        #  cursor.execute("COMMIT")
         cursor.close()
         con.commit()
         con.close()
         return iurl

def finddetailsofgivenurl(iurl):
    returnedData = getData(iurl)
    soup = BeautifulSoup(returnedData, 'html.parser')

    name = soup.find('h1', class_="firstHeading mw-first-heading", id="firstHeading")
    name=name.get_text()
    # print(name)

    link=soup.find('link', rel="canonical")
    link = link['href']
    # print(link)

    a=name.split()
    year=a[0]
    # print(year)

    hostcity = soup.find('td', class_="infobox-data location")
    hostcity=hostcity.get_text()
    # print(hostcity)

    participants=[]
    table = soup.find('table', class_="wikitable collapsible")
    grp=table.find_all('tr')
    grp=grp[1]
    list=grp.find_all('li')
    for a in list:
        country=a.find('a')
        participants.append(country.get_text())
    # print(participants)
    participants=listToString(participants)

    table = soup.find('table', class_="infobox")
    grp=table.find_all('tr')
    grp=grp[4]
    athlete=grp.find('td')
    athlete=athlete.get_text()
    # print(athlete)


    sports=[]
    table = soup.find('table', class_="multicol")
    if table:
        grp=table.find_all('td')
        # print(len(grp))
        for g in grp:
            list=g.find_all('li')
            for l in list:
                s=l.find('a')
                if s:
                    s=s.get_text()
                    if s != '':
                        sports.append(s)
    table = soup.find_all('div', class_="div-col")
    table=table[1]
    if table:
        list=table.find_all('li')
        for l in list:
            s=l.find('a')
            if s:
                s=s.get_text()
                if s != '':
                    sports.append(s)

    # print(sports)
    sports=listToString(sports)

    table = soup.find('table', class_="wikitable sortable plainrowheaders jquery-tablesorter")
    body=table.find('tbody')
    rows=body.find_all('tr')
    # print(rows[1])

    rank1=rows[1]
    w1=rank1.find('a')
    w1=w1.get_text()
    # print(w1)

    rank2=rows[2]
    w2=rank2.find('a')
    w2=w2.get_text()
    # print(w2)

    rank3=rows[3]
    w3=rank3.find('a')
    w3=w3.get_text()
    return name, link, year, hostcity, participants, athlete, sports, w1, w2, w3

     
# dbName = "OlympicsData.db"
# con, cursor = createDatabaseConnect(dbName)

# Update the Records where done is zero
while(True):
    dbName = "OlympicsData.db"
    url=giveurl(dbName)
    if url is None:
        sys.exit(1)

    name, link, year, hostcity, participants, athlete, sports, w1, w2, w3 = finddetailsofgivenurl(url)


    con, cursor = createDatabaseConnect(dbName)
    #NOW STORE THE VALUES OBTAINED INTO THE DATABASE
    # Execute the query with the parameters
    # print(f"process = {os.getpid()}")
    # print("\n")
    query = "UPDATE SummerOlympics SET Name = ?, Year = ?, HostCity = ?, ParticipatingNations = ?, Athletes = ?, Sports = ?, Rank_1_nation = ?, Rank_2_nation = ?, Rank_3_nation = ? WHERE WikipediaURL = ?;"
    cursor.execute(query, (name, year, hostcity, participants, athlete, sports, w1, w2, w3, url))
    # cursor.execute("COMMIT")
    con.commit()
    cursor.close()
    con.close()