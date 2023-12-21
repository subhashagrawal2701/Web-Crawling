# Web-Crawling
Historical Analysis and Visualization of Summer Olympic Games using Web Crawling

 Created a Web crawler using SQLite, Requests & Beautiful Soup in python
 Used SQLite database to store the fetched information.
 Parsed Wikipedia website to fetch Olympic Data for selected years.
 Extracted statistics from the obtained data – Average participants, Winning Nations Frequency etc.

# Collecting, Storing & Processing Unstructured Data
 Your task is to collect information about the different summer olympics from its Wikipedia page and
 process the data using Python’s urllib3 / requests (to get data) and BeautifulSoup library (for
 parsing/processing), and store the collected data in a SQLite database.
 TASK:
 1. Collect the main page of SummerOlympicsWikipedia for this task, the page is here:
 https://en.wikipedia.org/wiki/Summer_Olympic_Games . Note that you might need to use
 headers for fetching this page.
 2. NowcreateadatabaseCreate aSQLite database named ‘OlympicsData.db’ and a table
 named‘SummerOlympics’withthefollowing columns:
 ○ Name(e.g.“2012SummerOlympics”,intitle of respective wikipedia pages)
 ○ WikipediaURL
 ○ Year (theyearwhenitsconducted)
 ○ HostCity (thecity whereits hosted)
 ○ ParticipatingNations (List of the participating nations)
 ○ Athletes(numberofathletes)
 ○ Sports (list of sports)
 ○ Rank_1_nation
 ○ Rank_2_nation
 ○ Rank_3_nation
 3. Parsethehtmlfromstep1andextract the individual summer olympics wiki page urls for
 random2olympics fromthe last 50 years, i.e., from 1968 to 2020. (hint: try to parse the
 “List of SummerOlympicGames”tabletogettheurls and use random.samplefor
 randomsampling)
 4. Foreachofthepagesofyourtwoselected summerolympics, extract the data (with the help
 of BeautifulSoup) mentioned in step 2 and insert in the database.
 5. Thenusingthedatabaseprint answers to the following questions:
 ○ Whataretheyearsyouchose?
 ○ Whatistheaveragenumberofcountriesparticipating in the two olympics?
 ○ Printtheoverlap(i.e., common nations) within <Rank_1_nation, Rank_2_nation and
 Rank_3_nation> for your chosen two years
