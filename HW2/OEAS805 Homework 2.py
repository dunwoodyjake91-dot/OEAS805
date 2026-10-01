# OEAS805 Homework 2
# Name: Jacob Dunwoody

# %% Load the packages needed for the analysis
import pandas as pd  # used for loading and analyzing tabular data
import seaborn as sns  # used for statistical graphs
import matplotlib.pyplot as plt  # used for creating and editing figures
import cartopy.crs as ccrs  # used for map projections
import cartopy.feature as cfeature  # used for adding map features


# %% Load the Coastal Cleanup dataset
infile = r'C:\Users\dunwo\OEAS805\HW2\International_Coastal_Cleanup.csv'
data = pd.read_csv(infile,
    sep=',',
    thousands=',',
    low_memory=False)

data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')
print(data.head()) # Display the first five rows

# %% [markdown]
# ## 1. Dataset Size & Structure
#
# The first step of the exploratory data analysis is to determine the size
# of the dataset, examine its column names, and identify the data types.
# Each row represents one observation, while each column represents a
# variable recorded for that observation.

# %%
# Examine the size and data types of the dataset

print(f'The dataset contains {data.shape[0]} rows and {data.shape[1]} columns.')
print('\nNumber of columns for each data type:')
print(data.dtypes.value_counts())

# %% [markdown]
# ### Dataset Size & Type Findings
#
# The dataset contains 77 observations and 53 variables. The dataset contains 47 integer
# variables, 4 decimal variables, 1 date variable, and 1 text variable.
# Most variables are number counts of collected trash.


# %% [markdown]
# ## 2. Missing Values
#
# Missing values are examined to determine whether every variable contains
# the same number of observations. Only columns containing at least one
# missing value are displayed below.

# %%
# Count the missing values in each column
missing_values = data.isna().sum()
missing_values = missing_values[missing_values > 0]

missing_summary =pd.DataFrame({'Missing Values': missing_values})
missing_summary= missing_summary.sort_values(
    by='Missing Values', ascending=False)
if missing_summary.empty:
    print('No missing values in the dataset.')
else:
    print(missing_summary)
# %% [markdown]
# ### Missing Values 
#
# No missing values were found. All 53 variables have observations for
# all 77 cleanup records. No rows or columns would need to be removed.



# %% [markdown]
# ## 3. Descriptive Statistics
#
# Descriptive statistics are calculated for five variables that summarize
# the scale of each cleanup event: total items, litter weight, volunteers,
# volunteer hours, and miles cleaned. The statistics include the mean,
# standard deviation, median, quartiles, minimum, and maximum.


# %%
# Select the primary variables for descriptive statistics

variables_of_interest = ['Total Items Collected','Total Pounds of Litter Collected',
                         'Number of Volunteers','Volunteer Hours','Number of Miles']

descriptive_statistics = data[variables_of_interest].describe().T
descriptive_statistics = descriptive_statistics.rename(columns={'50%': 'Median'})
summary_table = descriptive_statistics[
    ['count', 'mean', 'std', 'Median', 'min', '25%', '75%', 'max']].round(2)
summary_table.index = ['Items Collected','Litter Weight (lb)','Volunteers',
                       'Volunteer Hours','Miles Cleaned']
summary_table.columns = ['N', 'Mean', 'Std Dev', 'Median', 'Min', 'Q1', 'Q3', 'Max']
# (Q1 - 25th percentile)
# (Q3 - 75th percentile)
print(summary_table.to_string())


# %% [markdown]
# ### Descriptive-Statistics Findings
#
# A typical cleanup collected 851 items weighing 80 pounds. It involved
# 11 volunteers who contributed 22 total hours and covered 1 mile.
# The mean was higher than the median for all five variables, suggesting
# that a few large cleanup events increased the averages.



# %% [markdown]
# ## 4. Data Distributions
#
# Histograms are used to show how the cleanup measurements are distributed.
# They can reveal skewed data, common values, and unusually large events.

# %%
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()
for i, variable in enumerate(variables_of_interest):
    sns.histplot(data=data, x=variable, bins=15, ax=axes[i])
    axes[i].set_title(variable)
axes[5].remove() # Remove the unused sixth graph
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Histogram Results
#
# Most cleanup events had low values for items, litter weight, volunteers,
# volunteer hours, and miles cleaned. A small number of cleanup events had
# much higher values, creating the long right tail shown in each histogram.


# %% [markdown]
# ## 5. Outlier Analysis
#
# Boxplots are used to identify values that are unusually high or low
# compared with the rest of the dataset.

# %%
# Boxplots for the five cleanup variables

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()
for i, variable in enumerate(variables_of_interest):
    sns.boxplot(data=data, x=variable, ax=axes[i])
    axes[i].set_title(variable)
axes[5].remove()# Remove the unused sixth graph
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Outlier Findings
#
# All five variables had high-value outliers. Total items collected had 12 
# outliers, volunteer hours had 8, litter weight had 7,number of volunteers had 
# 5, and miles cleaned had 4.These values likely represent events that 
# were much larger than normal.


# %% [markdown]
# ## 6. Relationships Between Variables
#
# Scatterplots are used to examine whether cleanup measurements increase
# together. The red line shows the general direction of each relationship.

# %%
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
sns.regplot(
    data=data,
    x='Number of Volunteers',
    y='Volunteer Hours',
    ax=axes[0],
    ci=None,
    line_kws={'color': 'red'})
axes[0].set_title('Volunteers and Volunteer Hours')

sns.regplot(
    data=data,
    x='Volunteer Hours',
    y='Total Items Collected',
    ax=axes[1],
    ci=None,
    line_kws={'color': 'red'})
axes[1].set_title('Volunteer Hours and Items')

sns.regplot(
    data=data,
    x='Total Items Collected',
    y='Total Pounds of Litter Collected',
    ax=axes[2],
    ci=None,
    line_kws={'color': 'red'})
axes[2].set_title('Items and Litter Weight')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Scatter Plot Findings
#
# Cleanup events with more volunteers generally recorded more volunteer hours.
# This was the clearest positive relationship between the three scatterplots.
#
# More volunteer hours were also generally associated with more items collected.
# The number of items and litter weight also increased together, although this
# relationship had a lot more variation.


# %% [markdown]
# ## 7. Most Common Litter Item

# %%
item_data = data.loc[:, 'Cigarette Butts':'Plastic Pieces']
top_items = item_data.sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    x=top_items.values,
    y=top_items.index,
    color='steelblue')
plt.title('Ten Most Common Types of Litter')
plt.xlabel('Total Number Collected')
plt.ylabel('Litter Type')
plt.tight_layout()
plt.show() 

# %% [markdown]
# ### Common-Litter Findings
#
# Cigarette butts were the most common litter item, with 36,975 collected.
# Plastic pieces were second with 20,577, and followed by metal bottle caps
# with 18,894.


# %% [markdown]
# ## 8. Cleanup Results by Year
#
# The median number of items and pounds collected per cleanup are compared
# across years. Medians are used because the data has high # outliers.
# %%
data['Year'] = data['Date'].dt.year
yearly_medians = data.groupby('Year')[
    ['Total Items Collected', 'Total Pounds of Litter Collected']].median().reset_index()

# yearly bar graphs
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.barplot(
    data=yearly_medians,
    x='Year',
    y='Total Items Collected',
    color='steelblue',
    ax=axes[0])
axes[0].set_title('Median Items Collected per Cleanup')
axes[0].set_ylabel('Median Number of Items')

sns.barplot(
    data=yearly_medians,
    x='Year',
    y='Total Pounds of Litter Collected',
    color='steelblue',
    ax=axes[1])
axes[1].set_title('Median Litter Weight per Cleanup')
axes[1].set_ylabel('Median Pounds Collected')
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Yearly Findings
#
# Cleanup events in 2017 had the highest median number of items and the
# highest median litter weights. The 2018 cleanup events had the secondh ighest
# values for both measurements.Median litter weight was lower in 2022 and 2023,
# while median item countsincreased in 2022 before decreasing again in 2023.
#
# These Changes do not show that the amount of litter changed 
# because cleanup locations and conditions varied between years. The 2020 year was excluded 
# because this was covid.


# %% [markdown]
# ## 9. Conclusions
#
# The dataset contained 77 cleanup events and 53 variables with no missing
# values. A typical cleanup collected 851 items weighing 80 pounds, involved
# 11 volunteers contributing 22 volunteer hours, and covered 1 mile.
#
# The cleanup measurements were right skewed and contained some high value
# outliers. These values are kept because they likely represent large cleanup 
# events rather than errors.
#
# Cleanup events with more volunteers generally had more volunteer hours, and
# greater volunteer effort was generally associated with more items collected.
# Cigarette butts were the most common litter item, followed by plastic pieces
# and metal bottle caps.
#
# Cleanup results varied between years, with the highest median values occurring
# in 2017. The dataset does not contain geographic coordinates which would be intresting to 
# use and help make a spatial map of where trash was most concentrated. 