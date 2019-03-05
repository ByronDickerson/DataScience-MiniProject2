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
    title = 'Hashtag Frequencies in Time Chunk ' + str(chunk_index) + ' of 8'
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

