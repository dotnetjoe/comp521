#!/usr/bin/env python
# coding: utf-8

# <div style="text-align: center;">
# <h1>The University of North Carolina at Chapel Hill</h1>
# <h1>Comp 521 Files and Databases - Fall 2019</h1>
# <h1 style="font-size: 250%;">Problem Set #1</h1>
# <h1 style="font-size: 200%;">Version 1.0</h1>
# <h1>Issued Tuesday 09/03/2019; Due Tuesday 09/17/2019</h1>
# </div>
# 
# **Homework Information:** The answer cells in this notebook contain metadata that enable it to be automatically parsed. Thus, you must enter your answers *only* into the cells provided. Do not delete any answer cell and/or add a new one to replace it. If you do so by accident, download a new copy of the problem set's notebook and transfer your answers into it. You can introduce new 'coding' cells in an effort to test approaches to problems, however, these introduced cells will not be considered when grading.
# 
# Finally, some of the problems are probably too long to be done the night before the due date, so plan accordingly. Late problem sets will be accepted, but your lowest problem-set grade will be dropped. Feel free to get help from others, but the work you submit in should be your own.

# In[1]:


# Do not make any edits in this cell!
class Student:
    first = "Adam"
    last = "Alston"
    onyen = "aalston9"
    pid = "730015776"


# The following questions relate to the design of a schema for an NFL database.
# Your primary data is provided in two downloadable text files. The first, is called <a href="https://csbio.unc.edu/mcmillan/Media/NFLrosters.csv">"NFLrosters.csv"</a> and has the following format:
# <pre><code style="font-size:80%;">
# team,year,jersey,name,position,height,weight,games,starts,college,dob,draftYear,draftRound,draftOrder,draftTeam
# carolina-panthers,2003,52,Brian Allen,LB,6-3,215,14,4,Florida State,--,--,--,--,--
# carolina-panthers,2003,80,Eugene Baker,WR,6-2,183,1,0,Kent State,1976-03-18,1999,5,164,atlanta-falcons
# carolina-panthers,2003,47,Marco Battaglia,TE,6-3,250,2,0,Rutgers,1973-01-25,1996,2,39,cincinnati-bengals
# carolina-panthers,2003,--,Nathan Black,WR,6-0,190,0,0,Northwestern State,1978-06-20,--,--,--,--
# carolina-panthers,2003,28,Colin Branch,DB,6-0,203,16,0,Stanford,1980-03-02,2003,4,119,carolina-panthers
# carolina-panthers,2003,79,Doug Brzezinski,OG,6-4,305,1,0,Boston College,1976-03-11,1999,3,64,philadelphia-eagles
# carolina-panthers,2003,99,Brentson Buckner,DT,6-2,305,12,12,Clemson,1971-09-30,1994,2,50,pittsburgh-steelers
# carolina-panthers,2003,98,Shane Burton,DE,6-6,305,16,4,Tennessee,1974-01-18,1996,5,150,miami-dolphins
# carolina-panthers,2003,59,Mike Caldwell,LB,6-2,200,9,0,Middle Tennessee State,--,--,--,--,--
# carolina-panthers,2003,50,Vinny Ciurciu,LB,6-0,235,2,0,Boston College,1980-05-02,--,--,--,--
# carolina-panthers,2003,40,Jarrod Cooper,DB,6-0,210,12,0,Kansas State,1978-03-31,2001,5,143,carolina-panthers
#                  .
#                  .
#                  .
#     </code></pre>
# A roster is a list of the players on a given team in a given year.
#        Each row also includes information about the player, such as their jersey number, position,
#        and the number of games that they played in and started in the given year.
#        It also includes information related the college they attended and their draft order if applicable.
# The second file is called <a href="https://csbio.unc.edu/mcmillan/Media/NFLgames.csv">"NFLgames.csv"</a> and has the following format:
# <pre><code style="font-size:80%;">
# season,week,date,visitor,vScore,home,hScore,notes
# 2018,1,2018-09-06,atlanta-falcons,12,philadelphia-eagles,18,
# 2018,1,2018-09-09,buffalo-bills,3,baltimore-ravens,47,
# 2018,1,2018-09-09,cincinnati-bengals,34,indianapolis-colts,23,
# 2018,1,2018-09-09,pittsburgh-steelers,21,cleveland-browns,21,
# 2018,1,2018-09-09,houston-texans,20,new-england-patriots,27,
# 2018,1,2018-09-09,jacksonville-jaguars,20,new-york-giants,15,
# 2018,1,2018-09-09,tennessee-titans,20,miami-dolphins,27,
# 2018,1,2018-09-09,san-francisco-49ers,16,minnesota-vikings,24,
# 2018,1,2018-09-09,tampa-bay-buccaneers,48,new-orleans-saints,40,
# 2018,1,2018-09-09,kansas-city-chiefs,38,los-angeles-chargers,28,
#                  .
#                  .
#                  .
#     </code></pre>
# It provides the final score for every game played during the season.
#     The visiting and home teams names are also provided.
#     Regular season games are denoted by their week number, whereas the 'week' indicates
#     the playoff round in the post-season.
#     Special notes are included for some games.

# Assume a database with tables for the following entities: <b>Player</b>, <b>Team</b>, <b>Game</b>, and <b>Draft</b>.
# You can assume that each player is assigned a <em>player id</em> (PID) as a primary key.
# Likewise, each team is assigned a <em>team id</em> (TID) as a primary key.
# The primary key of the Game relation is a composite of the season, week, and hometeam's TID.
# The primary key of the Draft relation is a composite of the draftYear and draftOrder.

# ---
# **Problem 1:** What columns from NFLroster.csv and other Entities would you include in the Player table?
name,height,weight,college,dob
# ---
# **Problem 2:** How many distinct entries would be populated in the Player relation using NFLroster.csv?
3 
# name,college,dob
# ---
# **Problem 3:** What columns, either in part or in full, from NFLroster.csv would you include in the Team table? Consider that teams have historically changed both locations and mascots.
team,year
# ---
# **Problem 4:** What component of the Game table's composite key is a foreign key from another table? What does this imply with regard to inserting new Game table rows?
tid, it implies that the you need information about from the team table
# ---
# **Problem 5:** In how many regular season games did the home team win?
5907
# games where the home score was greater than the visitor score
# In[21]:


import pandas as pd

dataframe = pd.read_csv("NFLgames.csv")
dataframe


# In[57]:


homeWins = 0
for index, row in dataframe.iterrows(): # index is a number, row is a dictionary
 if (row["hScore"] > row["vScore"]):
     homeWins += 1
print(homeWins)


# ---
# **Problem 6:** How many entries in NFLroster.csv differ from another entry by only the year?
18960
# calculated rows in csv and then subtracted duplicate rows of every column except for year
# In[137]:


import pandas as pd

dataframe = pd.read_csv("NFLrosters.csv")
dataframe


# In[139]:


entries = dataframe.drop_duplicates(subset=['team','position','jersey','position','height','weight','games','starts','college','dob','draftYear','draftRound','draftOrder','draftTeam'])
print len(dataframe)
print len(entries)
differByOnlyYear = len(dataframe) - len(entries)
print differByOnlyYear


# ---
# The next series of question consider the two relations <b>PlayedFor</b> and <b>LocatedAt</b>.
# PlayedFor has a primary key composed of a season-year, a PID, and a TID, as well as other attributes.
# LocatedAt has a primary key composed of a season-year, and a TID, as well as other attributes.

# ---
# **Problem 7:** How would you modify or extend the LocatedAt and/or Team tables to allow Teams to change mascots?
I would modify the Team table to add a Mascot field. Mascot should be independent of location.
ALTER TABLE Team
ADD Mascot TEXT;
# ---
# **Problem 8:** Based on the data provided, estimate the size of the PlayedFor table. Explain your estimate.
98452
# The PlayedFor tabel should have an entry for every record in the NFLrosters file
# In[114]:


import pandas as pd

dataframe = pd.read_csv("NFLrosters.csv")
dataframe


# In[115]:


print len(dataframe)


# ---
# **Problem 9:** Based on the data provided, estimate the size of the LocatedAt table. Explain your estimate.
1230
# 32 teams, 41 years, every team should have an entry for every year
# estimate=32*41 
# In[117]:


import pandas as pd

dataframe = pd.read_csv("NFLgames.csv")
dataframe


# In[119]:


homeCnt = dataframe.home.value_counts()
print homeCnt
print len(homeCnt)
# there are 32 teams


# In[111]:


seasonCnt = dataframe.season.value_counts()
print len(seasonCnt)
# there are 41 rows which means there are 41 years


# In[113]:


playedForEst = len(homeCnt) * len(seasonCnt)
# Every team should have an entry for every year
print playedForEst


# ---
# **Problem 10:** Budding DBA Lee Hart has suggested placing the "position" field in the PlayedFor table rather than the Player table. What are the advantages or disadvantages of this modification?
Advantages: Depending on which team the player is playing for, they can change positions
Disadvantages: The position is not distinctly atttached to the player but instead the player's stint with a team

# Something that I did consider was that players sometimes play more than one position at the same time. Neither before or after the modification could this property be specified in either table. So I think that is something to consider moving forward.
# ---
# **Problem 11:** Budding DBA Lee Hart has suggested placing the "jersey" field in the PlayedFor table rather than the Player table. What are the advantages or disadvantages of this modification?
Advantages: When a player switches teams, they do not always keep the same number so this would allow for the player to change numbers if they weren't allowed to before the modication
Disadvantages: Sometimes multiple people on the same team have the same number. You could no longer use the jersey number as an identifier of the player. You would need more information to go along with it.
# ---
# **Problem 12:** A roster player might become injured and spend part of a season in a special injured reserve list. How would you modify the given schema to capture this relation?
I would add a column to the PlayedFor table caller ir (injured reserve) and update that column accordingly.
ALTER TABLE PlayedFor
ADD COLUMN ir: TEXT
# ...
# For the next series of questions enter valid SQL statements.
# In some cases you will need to reference PIDs and TIDs using the helper functions
# getPID(name,dob,college) and getTID(teamName,year) respectively.

# ---
# **Problem 13:** Give the CREATE TABLE command for your implementation of the Team table. Include all primary and foriegn key declarions as well as any unique constraints.
CREATE TABLE Team (
    tid INTEGER,
    name TEXT,
    mascot TEXT,
    PRIMARY KEY (tid)
)
# ---
# **Problem 14:** Give the CREATE TABLE command for your implementation of the Game table. Include all primary and foriegn key declarions as well as any unique constraints.
CREATE TABLE Game (
    season INTEGER,
    week INTEGER,
    tid INTEGER,
    date DATE,
    vtid INTEGER,
    vscore INTEGER,
    hscore INTEGER,
    notes TEXT,
    PRIMARY KEY(season,week,tid),
    FOREIGN KEY(tid) REFERENCES Team(tid)
)
# ---
# **Problem 15:** Give the CREATE TABLE command for your implementation of the Draft table. Include all primary and foriegn key declarions as well as any unique constraints.
CREATE TABLE Draft (
    draftYear YEAR,
    draftOrder INTEGER,
    pid INTEGER,
    tid INTEGER,
    PRIMARY KEY(draftYear, draftOrder),
    FOREIGN KEY(pid) REFERENCES Player(pid)
    FOREIGN KEY(tid) REFERENCES Team(tid)
)
# ---
# **Problem 16:** Give an INSERT command that adds 'Jacoby Brissett' to your Player table. Use actual data from NFLroster.csv.
INSERT INTO Player
    VALUES (PID,'Jacoby Brisett',6-4,231,'North Carolina State',1993-12-11)
# In[146]:


import pandas as pd

dataframe = pd.read_csv("NFLrosters.csv")
dataframe


# In[148]:


for index, row in dataframe.iterrows(): # index is a number, row is a dictionary
 if (row["name"] == "Jacoby Brissett"):
    print row
    break


# ---
# **Problem 17:** Give INSERT commands that add 'Los Vegas Raiders' to your Team and LocatedAt tables. Assume that a TID is automatically created on any insert to the Team table.
INSERT INTO Team
VALUES (TID,'Los Vegas Raiders','Raiders')
INSERT INTO LocatedAt
VALUES (2020,TID)
# In[149]:


import pandas as pd

dataframe = pd.read_csv("NFLrosters.csv")
dataframe


# In[152]:


for index, row in dataframe.iterrows(): # index is a number, row is a dictionary
 if (row["team"] == "oakland-raiders"):
    print row
    break


# ---
# **Problem 18:** Give INSERT commands that add 'Baltimore Colts' to your Team and LocatedAt tables. Assume that a TID is automatically created on any insert to the Team table.
INSERT INTO Team
    VALUES (TID, 'baltimore-colts','colts')
INSERT INTO LocatedAt
    VALUES (TID,1960,'Baltimore')
# In[168]:


import pandas as pd

dataframe = pd.read_csv("NFLgames.csv")
dataframe


# In[171]:


for index, row in dataframe.iterrows(): # index is a number, row is a dictionary
 if (row["team"] == "baltimore-colts"):
    print row
    break


# ---
# **Problem 19:** Give an INSERT command that adds the score of 2012 American Conference Championship (played in 2013) to the Game tables. Use actual data from NFLgames.csv.
INSERT INTO Game
    VALUES (2012,'Conference Championship',TID,2013-01-20,vTID,28,13,NaN)
# In[156]:


import pandas as pd

dataframe = pd.read_csv("NFLgames.csv")
dataframe


# In[160]:


for index, row in dataframe.iterrows(): # index is a number, row is a dictionary
 if (row["week"] == "Conference Championship"):
    if (row["season"] == 2012):
        print row


# ---
# **Problem 20:** Give INSERT commands that add records for 'Jason Myers' to the PlayedFor tables. Use actual data from NFLroster.csv.
INSERT INTO PlayedFor (pid tid year position jersey games starts
    VALUES (PID,TID,2015,'K',2,16,0),
    VALUES (PID,TID,2015,'K',2,16,0),
    VALUES (PID,TID,2015,'K',2,6,0),
    VALUES (PID,TID,2015,'K',2,16,0),
    VALUES (PID,TID,2019,'K',5,0,0)
# In[163]:


import pandas as pd

dataframe = pd.read_csv("NFLrosters.csv")
dataframe


# In[165]:


for index, row in dataframe.iterrows(): # index is a number, row is a dictionary
 if (row["name"] == "Jason Myers"):
        print row


# Click [here to submit](http://csbio.unc.edu/mcmillan/index.py?run=PS.upload) your completed problem set.
# 
# You can submit it as many times as you would like, but only the last submitted version will be graded. If the last submission was after the due date the final score will be reduced accordingly. 

# In[ ]:




