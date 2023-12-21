import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random

#HELPER FUNCTION TO TO CONVERT LIST TO STRINGS
def listToString(s):

	# initialize an empty string
	str1 = ""

	# traverse in the string
	for ele in s:
		str1 += ele

	# return string
	return str1



#------------------------------------FETCH PAGE : PART 1------------------------
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

url = 'https://en.wikipedia.org/wiki/Summer_Olympic_Games'
returnedData = getData(url)

#-----------------------------------DATABASE CREATED : PART 2----------------------------------------------------
def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur

dbName = "OlympicsData.db"
cursor = createDatabaseConnect(dbName)

## Now you can create Table and insert/select records from there
## Lets create a Table "example" with three columns a, b and c to insert the structured data 
## we fecthed earlier
#DROP PREVIOUS TABLE
query="DROP TABLE IF EXISTS SummerOlympics"
cursor.execute(query)

query = "CREATE TABLE SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Athletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation)"
# query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Athletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation)"
cursor.execute(query)

#-----------------------------PART 3  SCRAPING THE PAGE TO GET URLS------------------------------------------------


soup = BeautifulSoup(returnedData, 'html.parser')

# SEARCH THE TABLE IN HTML WHICH HAS THE DATA
tables = soup.find_all('table', class_='sortable wikitable')


#TO STORE THE YEARS FOR WHICH DATA IS AVAILABLE
years=[]
for table in tables:
    # Iterate through table rows
    rows = table.find_all('tr')
    
    for row in rows:
        # Iterate through table cells (td elements) in each row
        cells = row.find_all(['td', 'th'])
        years.append(cells[0])
        
        # for cell in cells:
        #     # Print the text within the cell
        #     print(cell.get_text().strip())
years=years[18:]
years=years[:-4]
# print(years)
years.pop(len(years)-2)


#RANDOMLY SELECT ANY TWO YEARS
selectedyears= random.sample(years, 2)
# print(selectedyears)


#FETCH THE ROW OF THOSE TWO SELECTED YEARS
selectedtrows=[]
for table in tables:
    # Iterate through table rows
    rows = table.find_all('tr')
    for row in rows:
        # Iterate through table cells (td elements) in each row
        cells = row.find_all(['td', 'th'])
        # print(cells)
        if cells[0] in selectedyears:
            selectedtrows.append(row)
# print(selectedtrows)


#urls tags OF THOSE YEARS  // a herf.....
urls=[]
for row in selectedtrows:
    # Iterate through table cells (td elements) in each row
    cells = row.find_all(['td', 'th'])
    ur=cells[1].find('a')
    url = ur['href']
    urls.append(url)
# print(urls)



#--------------------------------SCRAPING THE FETCHED URLS----PART 4-------------------------

for url in urls:
    url_selected="https://en.wikipedia.org"+url
    # print(a)
    returnedData_selected = getData(url_selected)

    soup = BeautifulSoup(returnedData_selected, 'html.parser')

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
    # print(w3)

    # query = "INSERT INTO SummerOlympics VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(name, link, year, hostcity, participants, athlete, sports, w1, w2, w3)
    # cursor.execute(query)
    # cursor.execute("COMMIT")
    query = "INSERT INTO SummerOlympics (Name, WikipediaURL, Year, HostCity, ParticipatingNations, Athletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (name, link, year, hostcity, participants, athlete, sports, w1, w2, w3))
    cursor.execute("COMMIT")


#-----------------------------------------------STEP 5---------------------------------------------
#years
query="SELECT Year FROM SummerOlympics"
year=cursor.execute(query)
print("Chosen Years")
for row in year:
	print(row)
     
query="SELECT ParticipatingNations FROM SummerOlympics"
year=cursor.execute(query)
sum=0
for row in year:
    a=str(row).split()
    sum=sum+len(a)
print("Average No. Of Countries",sum/2)


query = "SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation FROM SummerOlympics"
cursor.execute(query)
# Fetch all the rows as a list of tuples
rankers = cursor.fetchall()
y1=set(rankers[0])
y2=set(rankers[1])
# print(rankers[0])
# print(y1,y2)
Intersection = y1.intersection(y2)
print("Overlap - Common Nations : ",Intersection)

