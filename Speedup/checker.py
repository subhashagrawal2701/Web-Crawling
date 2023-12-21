import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random
import sys
import time

#To Connect to Database
def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return con, cur

# def pri():
#     #Years that were Chosen
#     query="SELECT Year FROM SummerOlympics"
#     year=cursor.execute(query)
#     print("Chosen Years")
#     for row in year:
#         row=str(row)
#         row=row[2:6]
#         print(row)

#     #country that was ranker holder fom max no of time
#     print("\nCountry that was within top 3 for the maximum time in the database?")
#     query = "SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation FROM SummerOlympics WHERE DONE_OR_NOT_DONE is not 0"
#     rankers=cursor.execute(query)
#     dict={}
#     for row in rankers:
#          li=list(row)
#          for nation in li:
#               if nation in dict:
#                    dict[nation]=dict[nation]+1
#               else:
#                    dict[nation]=1
#         #  print(li,"\n\n")
#     # print(dict)
#     sorted_labels = sorted(dict, key=lambda k: dict[k], reverse=True)[:3]
#     print(sorted_labels)
    

#     #AVERAGE NO OF ATHLETES
#     query="SELECT Athletes FROM SummerOlympics WHERE DONE_OR_NOT_DONE is not 0"
#     athletes=cursor.execute(query)
#     count=0
#     sum=0
#     print("\nAverage No. Of Athletes")
#     for row in athletes:
#          count=count+1
#          s=str(row)
#          s=s[2:]
#         #  s=s[0].replace("[", " [")
#          s=s.split()
#          s=s[0].split("[")
#          s=s[0].replace(",", "")
#         #  print("---------",s)
#         #  print(s)
#          sum=sum+int(s)
#     if count !=0:
#         print(sum/count)

# while(True):
#     dbName = "OlympicsData.db"
#     con, cursor = createDatabaseConnect(dbName)
#     query="SELECT * from SummerOlympics WHERE DONE_OR_NOT_DONE = 0 or Name is null"
#     result = cursor.execute(query)
#     if result:
#          time.sleep(3)
#     else:
#          pri()
#     cursor.close()
#     con.close()
#     break;
         

dbName = "OlympicsData.db"
con, cursor = createDatabaseConnect(dbName)

#To CHECK if the All the rows are computed or not
query = "SELECT * from SummerOlympics WHERE DONE_OR_NOT_DONE = 0"
result = cursor.execute(query)
#TO CHECK IF QUERY OUTPUT IS NULL
con, new_cursor = createDatabaseConnect(dbName)  # Create a new cursor
new_cursor.execute(query)
first = new_cursor.fetchone()  # Fetch the first row
new_cursor.close()

# IF ALL PROCESS ARE DONE, EVALUATE THE METRICS ELSE IF ALL PROCESS ARE NOT DONE, EXIT
if first is None:

    #Years that were Chosen
    query="SELECT DISTINCT Year FROM SummerOlympics"
    year=cursor.execute(query)
    print("Chosen Years")
    # print(year)
    # size_of_tuple = sys.getsizeof(year)
    # print(size_of_tuple)
    for row in year:
        row=str(row)
        row=row[2:6]
        print(row)

    #country that was ranker holder fom max no of time
    print("\nCountry that was within top 3 for the maximum time in the database?")
    query = "SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation FROM SummerOlympics WHERE DONE_OR_NOT_DONE is not 0"
    rankers=cursor.execute(query)
    dict={}
    for row in rankers:
         li=list(row)
         for nation in li:
              if nation in dict:
                   dict[nation]=dict[nation]+1
              else:
                   dict[nation]=1
        #  print(li,"\n\n")
    # print(dict)
    sorted_labels = sorted(dict, key=lambda k: dict[k], reverse=True)[:1]
    print(sorted_labels)
    

    #AVERAGE NO OF ATHLETES
    query="SELECT Athletes FROM SummerOlympics WHERE DONE_OR_NOT_DONE is not 0"
    athletes=cursor.execute(query)
    count=0
    sum=0
    print("\nAverage No. Of Athletes")
    for row in athletes:
         count=count+1
         s=str(row)
         s=s[2:]
        #  s=s[0].replace("[", " [")
         s=s.split()
         s=s[0].split("[")
         s=s[0].replace(",", "")
        #  print("---------",s)
        #  print(s)
         sum=sum+int(s)
    if count !=0:
        print(sum/count)

else:
    sys.exit(1)
    print("All Process Not Done")
cursor.close()