#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Final_Data.csv")
df2 = pd.read_csv("Caterer.csv")


# In[ ]:


# First 5 Data of Final_Data
df.head()


# In[ ]:


# Removes the column named "Unnamed: 0"
df.drop("Unnamed: 0",axis=1,inplace=True)


# In[ ]:


# Count the number of missing (null or NaN) values in each column
df.isnull().sum()


# In[ ]:


# Count the number of duplicate rows
df.duplicated().sum()


# In[ ]:


# Display a concise summary for quickly understanding its structure and contents
df.info()


# In[ ]:


# Provides a summary of statistical metrics for numerical columns
df.describe()


# In[ ]:


# Count the unique values in the column named "Flat Vacancy"
df["Flat Vacancy"].value_counts()


# In[ ]:


# Array or Name of the unique values in the column named "Flat Vacancy"
df["Flat Vacancy"].unique()


# In[ ]:


# Count the unique values in the column named "Donation"
df["Donation"].value_counts()


# In[ ]:


# calculates the unique values and their count for each column
for i in df:
    a = df[i].nunique()
    b = df[i].unique()    
    print("\nNo of unique Value in Column",i,"is :-", a)
    print("\n",b)


# In[ ]:


# Removes the column named "Owner's Spouse Name"
df.drop("Owner's Spouse Name", axis = 1 , inplace = True)


# In[ ]:


# Convert the values in the column into numeric format
df['No of Resident'] = pd.to_numeric(df['No of Resident'], errors='coerce')
df['Confirmed Members'] = pd.to_numeric(df['Confirmed Members'], errors='coerce')
df['Maintenance Amt']= pd.to_numeric(df['Maintenance Amt'],errors='coerce')


# In[ ]:


# Replace the string "-" with "NaN" in each column
for i in df:
    df[i].replace("-", "NaN", inplace=True)
    print(df)


# # Impute Missing Values in Flat Vacancy

# In[ ]:


# Modify the DataFrame based on a condition
df.loc[df["Availlability of owner"] == "Yes", "Flat Vacancy"] = 'Owned'
df.loc[df["Availlability of owner"] == "No", "Flat Vacancy"] = 'Vacant'

#   OR

# Modify the DataFrame based on a condition to both NaN and non-NaN Value
df["Flat Vacancy"] =np.where(df["Availlability of owner"] == "Yes","Owned","Vacant")


# In[ ]:


# Average of Maintenance Amount in list form
avg_maintenance_amt = df.groupby("Flat Area (sq.mt)")["Maintenance Amt"].mean().to_dict()
print(avg_maintenance_amt)


# In[ ]:


# First Five rows after Change
df.head()


# In[ ]:


# Median Value of Donation
df["Donation"].median()


# # Impute Missing Values in "Donation", "No of Resident", "Confirmed Members" with Median

# In[ ]:


# Replaces NaN values in the "Donation" column with 2500, while leaving non-NaN values unchanged
df["Donation"] = np.where(df["Donation"].isna(), 2500, df["Donation"])


# In[ ]:


# Replace NaN values with median Value
df["No of Resident"].fillna(df["No of Resident"].median(), inplace = True)
df["Confirmed Members"].fillna(df["Confirmed Members"].median(), inplace = True)


# # Impute Missing Values in "Origin of Owner" and "Availability of owner" with Mode (most frequent value)

# In[ ]:


# Replaces NaN values in the "Availlability of owner" column with the mode
df["Availlability of owner"].replace({"NaN":df["Availlability of owner"].mode()[0]}, inplace = True)
df["Origin of Owner"] = np.where(df["Origin"] == "NaN", df["Origin"].mode(), df["Origin"])


# In[ ]:


df["Origin"].value_counts()


# In[ ]:


# creates a new column "Outsiders", subtracting the "No of Resident" column from the "Confirmed Members"
df["Outsiders"] = df["Confirmed Members"] -  df["No of Resident"]


# In[ ]:


df.head()


# ## Assign new value to column created x and 0

# In[ ]:


# np.select function from the NumPy library to conditionally update the values in the "Outsiders" column
a = [df["Outsiders"] > 0, df["Outsiders"] <= 0]
b = ["x",0]
df["Outsiders"] = np.select(a,b)


# In[ ]:


df["Outsiders"].head()


# In[ ]:


# Making All Lowercase at once in all Column
df[["Origin", "Tenant or owner", "Availlability of owner", "Flat Vacancy"]] = df[["Origin", "Tenant or owner", "Availlability of owner", "Flat Vacancy"]].applymap(lambda x: x.lower())


# In[ ]:


# First letter of each word is capitalized
df['Owner Name'] = df['Owner Name'].str.title()


# In[ ]:


df['Owner Name'].head()


# In[ ]:


# Calculate the average number of residents per flat
avg_num_per_flat = round(df['No of Resident'].mean(),0)
print(avg_num_per_flat)


# In[ ]:


# Group the "Origin of Owner" column, retrieves the group corresponding to the value "bangalore"
group = df.groupby("Origin")
group.get_group("bangalore")


# ## Determine the distribution of residents by their place of origin

# In[ ]:


origin_dist = df['Origin'].value_counts()
print(origin_dist)


# ## Visualize the distribution of residents by origin using a bar plot

# In[ ]:


plt.figure(figsize=(10,5))
sns.barplot(x="Origin",y="No of Resident", data = df, estimator = sum, errorbar = None)
plt.title("Total Number of Resident in Each State")
plt.xticks(rotation=45)
plt.show()


# # Calculate the average flat area (in square meters)

# In[ ]:


df["Flat Area (sq.mt)"].mean()


# # Find the most common number of rooms in flats

# In[ ]:


df["No of Room"].mode()


# In[ ]:


plt.figure(figsize=(8,5))
sns.histplot(df["Flat Area (sq.mt)"])
plt.title("Distribution of Flat Areas (sq.mt)")
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


# # Calculate the percentage of residents' participation by dividing the 'Confirmed Members' by the 'No of Resident' columns and multiplying by 100 to get the percentage

# In[ ]:


participation = (df['Confirmed Members']/df['No of Resident']) * 100
plt.figure(figsize=(8,6))
sns.boxplot(x='Tenant or owner',y=participation,data = df)
plt.title = 'Participation percent'
plt.xlabel('Tenant/Owner')
plt.ylabel('Participation %')
plt.show()


# # Calculate the average donation and total Donation

# In[ ]:


avg_donation = df["Donation"].mean()
print(avg_donation)


# In[ ]:


total_donation = df["Donation"].sum()
print(total_donation)


# ## New list recommendations

# In[ ]:


# Recommendation according to suggestion

recommendations = []

if avg_donation >= 5000:
    recommendations.append('consider high budget')
else:
    recommendations.append('consider optimization')
    
if participation.mean() >= 70:
    recommendations.append('Good turnout')
else:
    recommendations.append('More outreach required') 
    
if total_donation >= 50000:
    recommendations.append('Sufficient budget')
else:
    recommendations.append('Low budget')

print(recommendations)


# ## Catering Cost Analysis

# In[ ]:


df2.isnull().sum()


# In[ ]:


df2.duplicated().sum()


# In[ ]:


df2.info()


# In[ ]:


df2.describe()


# In[ ]:


df2.drop("Unnamed: 0",axis=1,inplace=True)


# In[ ]:


# Highest rated and Most cost-effective decor and caterer

highest_rated_caterer = df2[df2['Rating']== df2['Rating'].max()]
print(highest_rated_caterer.to_string(index=False))

cost_effective_caterer = df2[df2['Decoration Price']== df2['Decoration Price'].min()]
print(cost_effective_caterer.to_string(index=False))

cost_effective_caterer = df2[df2['Plate Cost']== df2['Plate Cost'].min()]
print(cost_effective_caterer.to_string(index=False))


# In[ ]:




