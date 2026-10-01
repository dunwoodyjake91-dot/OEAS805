#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis (EDA) example
# 
# This notebook will run through some of the basic analyses that you would typically do during EDA to get to know your data better. In this example, we will use data on the daily temperature in major global cities that can be downloaded from here: 
# https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities
# 
# The data were originally sourced from the National Climatic Data Center, compiled by the University of Dayton. More info and data descriptions and documentation can be found here:
# https://academic.udayton.edu/kissock/http/Weather/default.htm
# 
# I've added the `city_temperature.csv` file to the `data` folder in the course repository.

# In[11]:


# Load the packages needed for the analysis

import pandas as pd  # Data analysis and manipulation
import seaborn as sns  # Data visualization
import matplotlib.pyplot as plt  # Plotting and formatting


# In[12]:

# Load the CSV file containing city temperatures

# Path to the file on your computer
infile = r'C:\Users\dunwo\OEAS805\HW2\city_temperature.csv'
# Read the CSV file
data = pd.read_csv(infile, sep=',', low_memory=False)


# In[13]:


# convert the temperature data from F to C
# assign to a new column in the dataframe called 'AvgTemperatureC'
data['AvgTemperatureC'] = (data.AvgTemperature - 32) * 5/9
# print(data.AvgTemperature)
print(data.AvgTemperatureC)


# In[14]:


# print the information about the data in the dataframe
data.info()


# In[15]:


# the shape of the data
# nrows, ncols

data.shape


# In[16]:


# total number of datapoints in the dataframe
# ncol * nrows

data.size


# In[17]:


# gives a list of the column names in the dataframe

data.columns


# In[18]:


# descriptive statistics for the numeric data in the dataframe

data.describe()


# In[19]:


# correlations between the different numeric data columns in the dataframe

data.corr(numeric_only = True)


# In[20]:


# get a list of the unique values found in the 'City' column of the dataframe
data['City'].unique()

# assign the list of unique values of 'City' to a new variable called 'cities'
cities = data['City'].unique()


# In[21]:


print(cities[99:112])


# In[22]:


# Group the data by a particular column
# In this case, the data is grouped by country, and I am only interested in the 'City' column

data.groupby('Country')['City'].unique()


# In[23]:


fig, ax = plt.subplots(1, figsize = (20,8), dpi = 300)

sns.barplot(data = data, x = 'City', y = 'AvgTemperatureC')
ax.tick_params(axis='x', rotation=90)


# In[24]:


data.Year.unique()


# In[25]:


# histograms are the best, fastest data "check" for single variables
# in matplotlib, this is plt.hist

fig, ax = plt.subplots(1, figsize = (8,8), dpi = 300)
plt.hist(data["AvgTemperatureC"].dropna(), bins=20, color="steelblue", edgecolor="black")
plt.title("Histogram of AvgTemperatureC")
plt.xlabel("AvgTemperatureC")
plt.ylabel("Frequency")
plt.show()


# In[ ]: 




