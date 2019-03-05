
# coding: utf-8

# In[15]:


'''
#Stem has a lot more data points overall than the other hashtags, so the 'stem' points
in the scatter plot will often appear further above the points of other hashtags.

Across all hashtags, the frequency is lower in the early hours of the morning when
people are sleeping.

The strongest correlation appears between #csforall and #yolo between hours 36 and 42,
which is not a very enlightening piece of information.

'''
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import copy
import datetime
import tweepy

#f = open('tokens.txt', 'r')
consumer_key = 'fJXwpcMkXkRxjmrg0XJSLPDpO'
consumer_secret = 'xSuwqxYdVGYuUB5BUDSFOuaHxWE200PloiTzolQ39leD9EXb70' 
app_key = '1098671228813017089-lIzqXfUlCcvpMJP0D3BiHuH4GKaNQW'
app_secret = 'rqtPWfyrgGdvoRap9oxt8ptntuc7UPtInvWy4FPCi010t'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(app_key, app_secret)
api = tweepy.API(auth)


# In[ ]:


#uses OAuth which is pretty standard

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)# handshake

auth.set_access_token(app_key,app_secret) #access to timeline of the account

api = tweepy.API(auth, wait_on_rate_limit=True) #send it all in to get the API object

#reads in csv files and merges the two days for each hashtag
def mergeDFs(file1,file2):
    temp1 = pd.read_csv(f'{file1}.csv')
    temp2 = pd.read_csv(f'{file2}.csv')
    return pd.concat([temp1,temp2])

#reference for df.loc[...]
#https://stackoverflow.com/questions/15741759/find-maximum-value-of-a-column-and-return-the-corresponding-row-values-using-pan
def followers(df):
    df = df.reset_index()
    temp = df.loc[df['Followers'].idxmax()]
    print(f'{temp["Followers"]}\t\t@{temp["User"]}')
    
def retweets(df):
    df = df.reset_index()
    temp = df.loc[df['RTs'].idxmax()]
    printTweet(temp["ID"])

def favorites(df):
    df = df.reset_index()
    temp = df.loc[df['Favorites'].idxmax()]
    printTweet(temp["ID"])
    
#grabs tweet by ID and prints out information about it
def printTweet(id):
    #ID
    #@user:
    #text
    #RTs
    #Favs
    
    tweet = api.get_status(id)._json#['text']
    print(f'Tweet ID: {id}')
    print(f"{tweet['user']['name']}\t@{tweet['user']['screen_name']}")
    print(tweet['text'])
    print(f'RTs: {tweet["retweet_count"]}\t\tFavorites: {tweet["favorite_count"]}')


def makeDatetime(date):
    if type(date) == str:
        date = date.split()
        year = int(date[5])
        month = 2 #it's always february dont worry about it
        day = int(date[2])
        time = date[3].split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])

        return datetime.datetime(year, month, day, hour, minute, second)
          
          
# dataframe formatting. each hashtag is its own dataframe.
stem = mergeDFs('stem_27','stem_28').reset_index()
csforall = mergeDFs('csforall_27','csforall_28').reset_index()
equality = mergeDFs('equality_27','equality_28').reset_index()
yolo = mergeDFs('yolo_27','yolo_28').reset_index()


          
# Convert date strings into datetime objects.
# Reference for apply(lambda x...)
#https://stackoverflow.com/questions/34962104/pandas-how-can-i-use-the-apply-function-for-a-single-column
stem["time created"] = stem["time created"].apply(lambda x: makeDatetime(x))
csforall["time created"] = csforall["time created"].apply(lambda x: makeDatetime(x))
equality["time created"] = equality["time created"].apply(lambda x: makeDatetime(x))
yolo["time created"] = yolo["time created"].apply(lambda x: makeDatetime(x))

print('\n******************************************************************************************************************')

print('Most frequent user per hashtag:')
print(f'#stem\t\t{stem["User"].mode()[0]}')
print(f'#csforall\t{csforall["User"].mode()[0]}')
print(f'#equality\t{equality["User"].mode()[0]}')
print(f'#yolo\t\t{yolo["User"].mode()[0]}')
      

print('\nUser with the most followers, per hashtag:')
print('#stem\t\t',end='')
followers(stem)
print('#csforall\t',end='')
followers(csforall)
print('#equality\t',end='')
followers(equality)
print('#yolo\t\t',end='')
followers(yolo)

print('\nTweet with most retweets per hashtag:')
print('#stem')
retweets(stem)
print('\n#csforall')
retweets(csforall)
print('\n#equality')
retweets(equality)
print('\n#yolo')
retweets(yolo)

      
print('\nTweet with most favorites per hashtag:')
print('#stem')
favorites(stem)
print('\n#csforall')
favorites(csforall)
print('\n#equality')
favorites(equality)
print('\n#yolo')
favorites(yolo)
print('\n******************************************************************************************************************')



#bar charts!
# x axis: time from 00:00 to 05:59, in intervals of 00:15 minutes. so 24 ticks.
#y axis is the number of tweets in that 15-minute time frame. so if there weere 3 yolo tweets between 00:00 and 00:15, then the point would be (00:15,3)
#Only 1 data point per xtick. 

# so for the first bullet we want len(test.index) to be the value.

from matplotlib.dates import DateFormatter 
import matplotlib.dates as mdates
import matplotlib
import time

#matplotlib.rcParams['figure.figsize'] = [15, 10]

#constant
delta = datetime.timedelta(minutes=15) #add this each time youdhssdnfgbbkgnh
bigdelta = datetime.timedelta(hours=6)

time1 = datetime.datetime(2019, 2, 27, 0,0, 0)


#this is the first chunk. we need 8 of these.


def create_axes(d1,data):
    global bigdelta
    merged_data = []
    d2 = d1 + bigdelta
    for i in range(8):
        temp = data[data["time created"].between(d1,d2,inclusive=True)] #should we make inclusive false?

        #increment the time range by 15 minutes
        d1 = d2
        d2 += bigdelta

        #print(f'At time {d1} we have {len(temp.index)}')

        # add the Date(biggest end) and the Number Of Occurences 
        timestr = str(d1.month)+ '/' +str(d1.day) + ' ' + str(d1.hour) + ':00'
        merged_data.append([timestr,len(temp.index)])
        #print(timestr)
    return merged_data

axes_stem     = create_axes(time1, stem)
axes_csforall = create_axes(time1, csforall)
axes_equality = create_axes(time1, equality)
axes_yolo     = create_axes(time1, yolo)

df_bar_stem     = pd.DataFrame(axes_stem,     columns= ['time created','Frequency'])    
df_bar_csforall = pd.DataFrame(axes_csforall, columns = ['time created','Frequency'])
df_bar_equality = pd.DataFrame(axes_equality, columns = ['time created','Frequency'])
df_bar_yolo     = pd.DataFrame(axes_yolo,     columns = ['time created','Frequency'])

#print(df_bar_stem)


import random

c = (0.4, 0.4, 0.8,0.5)
c2 = (0.8, 0.4, 0.4,0.5)
c3 = (0.4, 0.8, 0.4,0.5)
c4 = (0.4, 0.4, 0.4,0.5)

ax  = df_bar_stem.plot.bar(    'time created', 'Frequency', color = c,  rot=60)
ax2 = df_bar_csforall.plot.bar('time created', 'Frequency', color = c2, rot=60)
ax3 = df_bar_equality.plot.bar('time created', 'Frequency', color = c3, rot=60)
ax4 = df_bar_yolo.plot.bar(    'time created', 'Frequency', color = c4, rot=60)


ax.set_ylabel('Frequency')
ax.set_title("#stem")

ax2.set_ylabel('Frequency')
ax2.set_title("#csforall")

ax3.set_ylabel('Frequency')
ax3.set_title("#equality")

ax4.set_ylabel('Frequency')
ax4.set_title("#yolo")




plt.show()

print('\n******************************************************************************************************************')

#!/usr/bin/env python
# coding: utf-8

# In[1]:


# imports

import pandas as pd
import matplotlib.pyplot as plt
import warnings

# supress warning (see later)
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[2]:


# import tweet data

csforall_27 = pd.read_csv("csforall_27.csv")
csforall_28 = pd.read_csv("csforall_28.csv")

equality_27 = pd.read_csv("equality_27.csv")
equality_28 = pd.read_csv("equality_28.csv")

stem_27 = pd.read_csv("stem_27.csv")
stem_28 = pd.read_csv("stem_28.csv")

yolo_27 = pd.read_csv("yolo_27.csv")
yolo_28 = pd.read_csv("yolo_28.csv")

csforall = pd.concat([csforall_27, csforall_28])
equality = pd.concat([equality_27, equality_28])
stem = pd.concat([stem_27, stem_28])
yolo = pd.concat([yolo_27, yolo_28])


# In[3]:


# split tweet time into a more useable format (separate timestamp into component elements, save day and time)

new = csforall["time created"].str.split(" ", expand = True) 
csforall["day"] = new[2]
csforall["time"] = new[3]

new = equality["time created"].str.split(" ", expand = True) 
equality["day"] = new[2]
equality["time"] = new[3]

new = stem["time created"].str.split(" ", expand = True) 
stem["day"] = new[2]
stem["time"] = new[3]

new = yolo["time created"].str.split(" ", expand = True) 
yolo["day"] = new[2]
yolo["time"] = new[3]


# In[4]:


# split tweet time into a more useable format, (separate time column into hours, min, sec; save hours, tens place of min)

new = csforall["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
csforall["hour"] = new[0]
csforall["min"] = new[4]

new = equality["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
equality["hour"] = new[0]
equality["min"] = new[4]

new = stem["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
stem["hour"] = new[0]
stem["min"] = new[4]

new = yolo["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
yolo["hour"] = new[0]
yolo["min"] = new[4]


# In[5]:


# period = day/hour/min, format: ddhhm
# (we've only saved the tens place of the minutes)

csforall['period'] = pd.to_numeric(csforall[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))
equality['period'] = pd.to_numeric(equality[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))
stem['period'] = pd.to_numeric(stem[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))
yolo['period'] = pd.to_numeric(yolo[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))


# In[6]:


# compile freqencies over 6 hour chunks

# pull all yolo tweets from the first six hours of Feb 27th
#test = yolo.loc[(yolo['day'] == 27) & (yolo['hour'] >= 0) & (yolo['hour'] < 6)]
# the number of tweets in that time period
#len(test)

# compile ALL the frequencies
d = {'csforall': csforall['period'].value_counts(), 
     'equality': equality['period'].value_counts(), 
     'stem': stem['period'].value_counts(),
     'yolo': yolo['period'].value_counts()}

# put the frequencies into a dataframe, fill all nulls with 0
frequencies = pd.DataFrame(data=d).fillna(0)


# In[8]:


# Break the frequency count into 6 hour time chunks. Drop the rows it adds for nonexistent time ranges.
# this is the code that produces the warnings. It doesn't like how values like "27059" don't exist.

chunk1 = frequencies.loc[range(27000,27060)].dropna()
chunk2 = frequencies.loc[range(27060,27120)].dropna()
chunk3 = frequencies.loc[range(27120,27180)].dropna()
chunk4 = frequencies.loc[range(27180,27240)].dropna()
chunk5 = frequencies.loc[range(28000,28060)].dropna()
chunk6 = frequencies.loc[range(28060,28120)].dropna()
chunk7 = frequencies.loc[range(28120,28180)].dropna()
chunk8 = frequencies.loc[range(28180,28240)].dropna()

chunks = [chunk1, chunk2, chunk3, chunk4, chunk5, chunk6, chunk7, chunk8]


# In[9]:


chunk_index = 1     # for titling the scatterplots

# for each time chunk
for chunk in chunks:
    number = 1      # to add subplots to the figures correctly
    checklist = []  # to make sure we don't redraw identical graphs
    
    # Make and title a figure
    fig = plt.figure(figsize=(12,10))
    fig.subplots_adjust(wspace=0.25, hspace=0.5, left=0.125, right=0.9, top=0.9, bottom=0.1)
    title = 'Hashtag Frequencies from Hour ' + str(6*(chunk_index-1)) + ' to ' + str(6*(chunk_index-1)+6)   
    fig.suptitle(title, fontsize=16)
    chunk_index += 1
    
    # for each pair of hashtags (duplicates nonwithstanding)
    for hashtag in chunk:
        checklist.append(hashtag)
        for othertag in chunk:
            if othertag not in checklist:
                # draw a scatterplot comparing their frequencies and add it to the figure
                ax1 = fig.add_subplot(3,2,number)
                ax1.scatter(chunk.index, chunk[hashtag], c="b", marker="o", label = hashtag, alpha = .5)
                ax1.scatter(chunk.index, chunk[othertag], c='r', marker="s", label = othertag, alpha = .5)
                plt.legend(loc='upper left');
                ax1.set_xlabel('time')
                ax1.set_ylabel('frequency count')
                number += 1
    
    plt.show()
print('\n******************************************************************************************************************')

