import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random
import os
import time
import multiprocessing

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

#-----------------------------------DATABASE CREATED : PART 1b----------------------------------------------------
def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur, con

dbName = "OlympicsData.db"
cursor, con = createDatabaseConnect(dbName)

#DROP PREVIOUS TABLE
query="DROP TABLE IF EXISTS SummerOlympics"
cursor.execute(query)

query = "CREATE TABLE SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Athletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation, DONE_OR_NOT_DONE)"
# query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Athletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation)"
cursor.execute(query)

#-----------------------------PART 1c  SCRAPING THE PAGE TO GET URLS------------------------------------------------


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
        
years=years[18:]
years=years[:-4]
# print(years)
years.pop(len(years)-2)


#RANDOMLY SELECT ANY TWO YEARS
selectedyears= random.sample(years, 10)
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
    url="https://en.wikipedia.org"+url
    urls.append(url)
    query = "INSERT INTO SummerOlympics (WikipediaURL, DONE_OR_NOT_DONE) VALUES (?, ?)"
    cursor.execute(query, (url, 0))
    cursor.execute("COMMIT")
# print(urls)
if __name__=="__main__":
    start_time = time.time()
    p1=multiprocessing.Process(target=os.system, args=("python scraper.py",))
    # p2=multiprocessing.Process(target=os.system, args=("python scraper.py",))
    # p3=multiprocessing.Process(target=os.system, args=("python scraper.py",))
    p4=multiprocessing.Process(target=os.system, args=("python checker.py",))

    p1.start()
    # p2.start()
    # p3.start()
    p4.start()


    p1.join()
    # p2.join()
    # p3.join()
    p4.join()


    end_time= time.time()
    print("Time : {}ms".format(end_time-start_time))
    
    # end_time = time.time()
    # print("total time : ",end = ' ')
    # print(end_time-start_time)

# # Spawn three separate processes to run "scraper.py"
# for _ in range(3):
#     os.system("python scraper.py &")

os.system("python checker.py &")

# cursor.execute("COMMIT")
con.commit()
cursor.close()
con.close()


