#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Final_Data.csv")


# In[2]:


# First 5 Data
df.head()


# In[3]:


# Removes the column named "Unnamed: 0"
df.drop("Unnamed: 0",axis=1,inplace=True)


# In[4]:


# Count the number of missing (null or NaN) values in each column
df.isnull().sum()


# In[4]:


# Count the number of duplicate rows
df.duplicated().sum()


# In[6]:


# Display a concise summary for quickly understanding its structure and contents
df.info()


# In[7]:


# Provides a summary of statistical metrics for numerical columns
df.describe()


# In[8]:


# Count the unique values in the column named "Flat Vacancy"
df["Flat Vacancy"].value_counts()


# In[9]:


# Array or Name of the unique values in the column named "Flat Vacancy"
df["Flat Vacancy"].unique()


# In[10]:


# Count the unique values in the column named "Donation"
df["Donation"].value_counts()


# In[7]:


# calculates the unique values and their count for each column
for i in df:
    a = df[i].nunique()
    b = df[i].unique()    
    print("\nNo of unique Value in Column",i,"is :-", a)
    print("\n",b)


# In[10]:


# Replace the string "-" with "NaN" in each column
for i in df:
    df[i].replace("-", "NaN", inplace=True)
    print(df)


# In[14]:


# Removes the column named "Owner's Spouse Name"
df.drop("Owner's Spouse Name", axis = 1 , inplace = True)


# In[15]:


# Convert the values in the column into numeric format
df['No of Resident'] = pd.to_numeric(df['No of Resident'], errors='coerce')
df['Confirmed Members'] = pd.to_numeric(df['Confirmed Members'], errors='coerce')


# # Average of Maintenance Amt

# # Impute Missing Values in Flat Vacancy

# In[16]:


df.loc[df["Availlability of owner"] == "Yes", "Flat Vacancy"] = 'Owned'
df.loc[df["Availlability of owner"] == "No", "Flat Vacancy"] = 'Vacant'

#   OR

df["Flat Vacancy"] =np.where(df["Availlability of owner"] == "Yes","Owned","Vacant") #drawback it will change NaN value too


# In[17]:


df.head()


# In[18]:


df["Donation"].median()


# # Impute Missing Values in "Donation", "No of Resident", "Confirmed Members" with Median

# In[19]:


df["Donation"] = np.where(df["Donation"].isna(), 2500, df["Donation"])


# In[20]:


df["No of Resident"].fillna(df["No of Resident"].median(), inplace=True)


# In[21]:


df["Confirmed Members"].fillna(df["Confirmed Members"].median(), inplace = True)


# # Impute Missing Values in "Origin of Owner" and "Availability of owner" with Mode (most frequent value)

# In[22]:


df["Availlability of owner"].replace({"NaN":df["Availlability of owner"].mode()[0]}, inplace = True)


# In[23]:


df["Availlability of owner"].value_counts()


# In[24]:


df["Origin of Owner"] = np.where(df["Origin of Owner"] == "NaN", df["Origin of Owner"].mode(), df["Origin of Owner"])


# In[25]:


df["Origin of Owner"].value_counts()


# # Task 3

# ## Calculate Difference and Create New Column

# In[26]:


df["Outsiders"] = df["Confirmed Members"] -  df["No of Resident"]


# In[27]:


df.head()


# ## Assign new value to column created x and 0

# In[28]:


a = [df["Outsiders"] > 0, df["Outsiders"] <= 0]
b = ["x",0]
df["Outsiders"] = np.select(a,b)


# In[29]:


df["Outsiders"].head()


# # Making All Lowercase at once in all Column

# In[30]:


df[["Origin of Owner", "Tenant or owner", "Availlability of owner", "Flat Vacancy"]] = df[["Origin of Owner", "Tenant or owner", "Availlability of owner", "Flat Vacancy"]].applymap(lambda x: x.lower())


# In[31]:


df[["Origin of Owner", "Tenant or owner", "Availlability of owner", "Flat Vacancy"]].head()


# # first letter of each word is capitalized

# In[32]:


df['Owner Name'] = df['Owner Name'].str.title()   #first letter of each word is capitalized


# In[33]:


df['Owner Name'].head()


# # Task 5

# ## Calculate the average number of residents per flat

# In[34]:


df["Confirmed Members"]/df["No of Room"]


# In[35]:


df.head()


# In[36]:


group = df.groupby("Origin of Owner")
group.get_group("bangalore")


# ## Determine the distribution of residents by their place of origin

# In[37]:


pivot_t = df.pivot_table(values = "No of Resident", index = "Origin of Owner", aggfunc = "sum")
pivot_t


# ## Visualize the distribution of residents by origin using a bar plot

# In[44]:


plt.figure(figsize=(10,5))
sns.barplot(x="Origin of Owner",y="No of Resident", data = df)
plt.xticks(rotation=45)
plt.show()


# # Calculate the average flat area (in square meters)

# In[ ]:


df["Flat Area (sq.mt)"].mean()


# # Find the most common number of rooms in flats

# In[ ]:


df["No of Room"].mode()


# In[ ]:


plt.figure(figsize=(10,5))
sns.histplot(x="Origin of Owner",y=df["Flat Area (sq.mt)"].mean(), data = df, hue = df["Flat Area (sq.mt)"])
plt.xticks(rotation = 45)
plt.show()


# # Calculate the percentage of flat owners and tenants in the housing society and Show in Pie Shart

# In[ ]:


df["Tenant or owner"].value_counts()


# In[ ]:


df['Tenant or owner'].value_counts(normalize=True) * 100


# In[ ]:


plt.pie(df["Tenant or owner"].value_counts(), labels=df["Tenant or owner"].value_counts().index, autopct = "%1.1f%%",
       startangle = 90)


# # Task 6

# ## Calculate the percentage of residents' participation by dividing the 'Confirmed Members' by the 'No of Resident' columns and multiplying by 100 to get the percentage

# In[46]:


(df["No of Resident"]/df["No of Resident"].sum())*100


# In[47]:


df.head()


# In[56]:


plt.figure(figsize =(10,5))
plt.boxplot((df["No of Resident"]/df["No of Resident"].sum())*100)
plt.show()


# # Calculate the average donation and total Donation

# In[57]:


df["Donation"].mean()


# In[58]:


df["Donation"].sum()


# ## New list recommendations

# In[ ]:


list_a = [df["Donation"] >= 5000, df["Donation"].mean() > 0.70, df["Donation"] > 50000 ]
list_b = ["higher budget", "good turnout", "sufficient funds"]


# In[ ]:




