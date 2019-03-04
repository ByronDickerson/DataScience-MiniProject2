#!/usr/bin/env python
# coding: utf-8

# Answer this: what shape do you need your data?

# In[1]:


import  numpy as np
import pandas as pd
import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import confusion_matrix
from patsy import dmatrices, dmatrix
import matplotlib.pyplot as plt
from sklearn import datasets


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


# split tweet time into a more useable format, (separate time column into hours, min, sec; save hours, min)

new = csforall["time"].str.split(":", expand = True) 
csforall["hour"] = new[0]
#csforall["min"] = pd.to_numeric(new[1])

new = equality["time"].str.split(":", expand = True) 
equality["hour"] = new[0]
#equality["min"] = pd.to_numeric(new[1])

new = stem["time"].str.split(":", expand = True) 
stem["hour"] = new[0]
#stem["min"] = pd.to_numeric(new[1])

new = yolo["time"].str.split(":", expand = True) 
yolo["hour"] = new[0]
#yolo["min"] = pd.to_numeric(new[1])


# In[5]:


# period = day/hour, format: ddhh

csforall['period'] = pd.to_numeric(csforall[['day', 'hour']].apply(lambda x: ''.join(x), axis=1))
equality['period'] = pd.to_numeric(equality[['day', 'hour']].apply(lambda x: ''.join(x), axis=1))
stem['period'] = pd.to_numeric(stem[['day', 'hour']].apply(lambda x: ''.join(x), axis=1))
yolo['period'] = pd.to_numeric(yolo[['day', 'hour']].apply(lambda x: ''.join(x), axis=1))


# In[6]:


# drop unneccesary info (only period remains)

csforall.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time', 'day'],inplace=True,axis=1) 
equality.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time', 'day'],inplace=True,axis=1) 
stem.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time', 'day'],inplace=True,axis=1) 
yolo.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time', 'day'],inplace=True,axis=1) 


# In[7]:


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


chunk1 = frequencies.loc[range(2700,2706)]
chunk2 = frequencies.loc[range(2706,2712)]
chunk3 = frequencies.loc[range(2712,2718)]
chunk4 = frequencies.loc[range(2718,2724)]
chunk5 = frequencies.loc[range(2800,2806)]
chunk6 = frequencies.loc[range(2806,2812)]
chunk7 = frequencies.loc[range(2812,2818)]
chunk8 = frequencies.loc[range(2818,2824)]

chunks = [chunk1, chunk2, chunk3, chunk4, chunk5, chunk6, chunk7, chunk8]


# In[9]:


for chunk in chunks:
    fig = plt.figure(figsize=(12,6))
    fig.subplots_adjust(wspace=0.25, hspace=0.50, left=0.125, right=0.9, top=0.9, bottom=0.1)
    #title = ('Frequencies in time chunk', chunk)
    #fig.suptitle(title, fontsize=16)
    number = 1
    for hashtag in chunk:
        for othertag in chunk:
            if hashtag != othertag:
                ax1 = fig.add_subplot(4,3,number)
                ax1.scatter(chunk[hashtag], chunk[othertag], color="blue", marker="o", alpha=.4)
                ax1.set_xlabel(hashtag)
                ax1.set_ylabel(othertag)
                number += 1
    plt.show()


# In[10]:


fig = plt.figure(figsize=(12,6))

fig.subplots_adjust(wspace=0.25, hspace=0.50, left=0.125, right=0.9, top=0.9, bottom=0.1)
fig.suptitle('Frequencies, Feb 27, 00:00 to 06:00', fontsize=16)

number = 1

for hashtag in chunk1:
    for othertag in chunk1:
        if hashtag != othertag:
            ax1 = fig.add_subplot(4,3,number)
            ax1.scatter(chunk2[hashtag], chunk2[othertag], color="red", marker="o", alpha=.4)
            ax1.set_xlabel(hashtag)
            ax1.set_ylabel(othertag)
            number += 1

plt.show()

