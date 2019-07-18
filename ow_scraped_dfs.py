#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup


# In[2]:


with open('blizzard_data.html',encoding="utf-8") as html_file:
    soup = BeautifulSoup(html_file, 'lxml')


# <h2>Function takes "table_cols" from the main method as a parameter and returns a list of column headers for dataframe</h2>

# In[3]:


def get_col_heads(table_cols):
    col_heads = []
    for string in table_cols.strings:
        col_heads.append(string)
    return col_heads


# <h2> Function takes "rows" from main method as a parameter and returns a list full of list rows for dataframe</h2>

# In[4]:


def get_row_data(rows):
    row_data = []
    for row in rows:
        cells = row.findChildren('td')
        line = []
        for cell in cells:
            line.append(cell.string)
        row_data.append(line)
    return row_data


# <h2>All variables used in web scraping from HTML file</h2>

# In[5]:


#Scrape all h2 tags from html file and store in headers
headers = soup.find_all('h2')

#Lists to store column headers and data for each dataframe
pms_cols = []          #Player Map Stat column names
pms_row_data = []      #Player Map Stat row data
pahs_cols = []         #Player All Hero Stat column names
pahs_row_data = []     #Player All Hero Stat row data
hs_cols = []           #Hero Stat column names
hs_row_data = []       #Hero Stat row data


# <h2>"Main" Method</h2>

# In[6]:


#Loop through all heads in headers
for head in headers:
    if head.get_text() == "Player Map Stat":
        table = head.find_next_sibling('table')
        cols = table.find('thead')
        rows = cols.find_next_siblings('tr')
        pms_row_data = get_row_data(rows)
        pms_cols = get_col_heads(cols)
        
        
    #If header = Player All Hero Stat
    elif head.get_text() == "Player All Hero Stat":
        table = head.find_next_sibling('table')
        cols = table.find('thead')
        rows = cols.find_next_siblings('tr')
        pahs_row_data = get_row_data(rows)
        pahs_cols = get_col_heads(cols)
        
    #If header = Hero Stat
    elif head.get_text() == "Hero Stat":
        table = head.find_next_sibling('table')
        cols = table.find('thead')
        rows = cols.find_next_siblings('tr')
        hs_row_data = get_row_data(rows)
        hs_cols = get_col_heads(cols)


# <h2>Load <b>Player Map Stat</b> data into a dataframe</h2>

# In[7]:


pms_df = pd.DataFrame(pms_row_data, columns = pms_cols)
pms_df.head(10)


# <h2>Load <b>Player All Hero Stat</b> data into a dataframe</h2>

# In[8]:


pahs_df = pd.DataFrame(pahs_row_data, columns = pahs_cols)
pahs_df.head()


# <h2>Load <b>Hero Stat</b> data into a dataframe</h2>

# In[9]:


hs_df = pd.DataFrame(hs_row_data, columns = hs_cols)
hs_df.head()


# In[10]:


hs_df.dtypes


# <h2>Change appropriate columns in each table to floating point numbers</h2>

# In[11]:


pms_df['Amount'] = pd.to_numeric(pms_df['Amount'])
pahs_df['Amount'] = pd.to_numeric(pahs_df['Amount'])
hs_df['Amount'] = pd.to_numeric(hs_df['Amount'])


# <h2>Write all dataframes to a CSV file for data manipulation in other programs</h2>

# In[12]:


pms_df.to_csv('Player_Map_Stat.csv', index = None)
pahs_df.to_csv('Player_All_Hero_Stat.csv', index = None)
hs_df.to_csv('Hero_Stat.csv', index = None)

