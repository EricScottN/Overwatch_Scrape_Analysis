#!/usr/bin/env python
# coding: utf-8

# <h1><b>Web Scraping and Analysis of Overwatch Data to Discover Trends in Gameplay</b></h1>
# AC-201 / by: Buffalo-27

# In[1]:


import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from altair import Chart, X, Y, Color, Scale
import altair as alt


# <h2>Load data from .CSV's into individual Pandas Dataframes.</h2>

# Import the data stored from the web scraping notebook into their own respective dataframes for future analysis

# In[2]:


pms_df = pd.read_csv("Player_Map_Stat.csv")
pahs_df = pd.read_csv("Player_All_Hero_Stat.csv")
hs_df = pd.read_csv("Hero_Stat.csv")


# <h1>Cleaning up the Player Map Stat Dataframe</h1>

# <h2>Create a new DataFrame using only Unranked in Stat Context Type in Player Map Stat DataFrame</h2>

# All values under Stat Context Type are unranked, as that is the data I'm working with. Column data is now useless. Best to clean it up

# In[3]:


unranked_df = pms_df.loc[pms_df['Stat Context Type'] == 'Unranked']
unranked_df.head(10)


# <h2>Drop Stat Context Name and Stat Context Type columns</h2>

# Dropping the Stat Context Type, as I am examining unranked. I know these are all unranked games. Also, there is no Stat Context Name in this unstance as that relates to a different Stat Context Type. Removal of both will make data less redundant.

# In[4]:


unranked_df = unranked_df.drop(['Stat Context Name','Stat Context Type'], 1)
unranked_df.head(20)


# <h2>Use pivot_table function to place unique maps as indeces and all stats from Dataframe as columns</h2>

# The primary focus of this data is dependent on the map so a pivot table will clean up that data nicely.

# In[5]:


unranked_df = pd.pivot_table(unranked_df, values = 'Amount', index = 'Map', columns = 'Stat', fill_value = 0)
unranked_df


# <h2>Sort Maps By Highest Win Percentage</h2>

# Main objective - To be aware of maps that I excel at or have the best win percentage on. So a new column is created with that statistic. In this case, it is Busan. However, this map is one of the more recent maps released which I began playing when I was a better player. Rialto is the second most recent map.

# In[6]:


unranked_df['Win %'] = (unranked_df['Map Wins'] / unranked_df['Map Enters'] * 100)
unranked_df.sort_values(by='Win %', ascending = False)


# <h2>Create chart from data</h2>

# A chart to visualize my win percentages

# In[7]:


Chart(unranked_df.reset_index()).mark_bar().encode(
    x='Win %',
    y='Map'
)


# <h2>Create new DataFrame using Ranked data from Stat Context Type in Player All Hero Stat Dataframe</h2>

# Now to create some data on my ranked play throughout the various "seasons" of Overwatch. First is creating a new DataFrame using only ranked data from the Player All Hero Stat table.

# In[8]:


ranked_df = pahs_df.loc[pahs_df['Stat Context Type'] == 'Ranked']
ranked_df.head(10)


# <h1>Some more DataFrame cleanup</h1>

# <h2>Drop the Stat Context Type because it is useless information</h2>

# Just as with that Player Map Stat Dataframe, some redundant columns can be removed to make it look cleaner

# In[9]:


ranked_df = ranked_df.drop('Stat Context Type', 1)
ranked_df.head(5)


# May as well change the column name this time since we know what it is. The season numbers.

# In[10]:


ranked_df = ranked_df.rename(columns = {'Stat Context Name':'Season'})
ranked_df.head(5)


# For sake of clarity, remove the string "season" from the values in Season column. Additionally, change them to integers so they can be nicely placed on a chart later.

# In[11]:


ranked_df['Season'] = ranked_df['Season'].str[6:]
ranked_df["Season"] = pd.to_numeric(ranked_df["Season"], downcast = 'integer')
ranked_df.head(10)


# <h2>Another pivot table to better see the data depending on season number

# In[12]:


ranked_df = pd.pivot_table(ranked_df, values = 'Amount', index = 'Season', columns = 'Stat', fill_value = 0)
ranked_df


# <h2>Chart to visualize data</h2>

# For the most damage done in a single game, my best showing was seasons 10 and 11 and it's been mostly downhill from there. Time to step it up!

# In[13]:


alt.Chart(ranked_df.reset_index()).mark_line().encode(
    x='Season:O',
    y='All Damage Done - Most in Game'
)


# <h2>Create new DataFrame using only Mystery Heroes data</h2>

# Mystery Heroes picks random heroes for the player to use and is a very accurate representation of skill set with each character.

# In[14]:


mystery_heroes_df = hs_df.loc[hs_df['Stat Context Name'] == 'Mystery Heroes']
mystery_heroes_df.head(5)


# <h1>Database Cleanup</h1>

# Drop redundant columns

# In[15]:


mystery_heroes_df = mystery_heroes_df.drop('Stat Context Name', 1)
mystery_heroes_df = mystery_heroes_df.drop('Stat Context Type', 1)
mystery_heroes_df.head(5)


# <h2>MORE PIVOT TABLES!</h2>

# In[16]:


mystery_heroes_df = pd.pivot_table(mystery_heroes_df, values = 'Amount', index = 'Hero', columns = 'Stat', fill_value = 0)
mystery_heroes_df


# <h2>Generate chart of eliminations in the Mystery Heroes game mode</h2>

# D.Va is my best character. Given that each hero should have more or less been randomly selected, more eliminations were generated when playing as D.Va

# In[17]:


alt.Chart(mystery_heroes_df.reset_index()).mark_bar().encode(
    x='Hero',
    y='Eliminations',
)

