# GymDataAnalytics

Small learning project for data analytics.Were I tried to learn and improve my data manipulation skills as well anlyze data from synthetic dataset.

## About dataset
[Dataset](https://www.kaggle.com/datasets/mexwell/gym-check-ins-and-user-metadata) was taken from Kaggle and itself is synthetic.Dataset consists of four csv files.
Which are users_data,subscription_plans,gym_location_data,checkin_checkout_data.

## Libs Installation

Therefore to work with our data several libs needed to be installed.
They are shown under this text.
```bash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
```
### Libs usage in the project
Pandas is used for data manipulation and to read our csv files.

Seaborn is used with matplotlib to display our data.
## Defining dataframes
Dataframes are defined from four csv that we read with pandas.
```bash
df_checkin = pd.read_csv('checkin_checkout_history_updated.csv')
df_gym = pd.read_csv('gym_locations_data.csv')
df_sub = pd.read_csv('subscription_plans.csv')
df_user = pd.read_csv('users_data.csv')
```
## Data cleaning
This part describes the process of data cleaning in this project.
### Getting list of unique facilities
There were unnecessery values I wanted to remove.There were duplicates and some of them anyway should have been edited in future for consistency reasons.
```bash
flist = sorted(set(df_gym['facilities'].str.split().explode().str.strip()))

flist.remove('Classes')
flist.remove('Classes,')
flist.remove('Court')
flist.remove('Court,')
flist.remove('CrossFit,')
flist.remove('Pool')
flist.remove('Pool,')
flist.remove('Sauna,')
flist.remove('Wall,')
```
Then we create new column for each value.The column represents bool value of facility availability in certain gym.

```bash
for f in flist:
    df_gym[f] = df_gym['facilities'].str.contains(f,case=False,na=False)
```
Next part is to fix namings for each column.Here I assign new name to each column.

```bash
new_cols = {'Basketball':'basketball_court',
            'Climbing':'climbing_wall',
            'CrossFit':'crossfit',
            'Sauna':'sauna',
            'Swimming':'swimming_pool',
            'Yoga':'yoga_classes'
}
df = df.rename(new_cols,axis=1)
```
### Joining all of the data
Here I join all four csv tables together for easier workflow.
To create main dataframe df we start by merging df_user with df_sub by their joint column 'subscription_plan'.
Similar for df_checkin we merge with previous merge by joint 'user_id'.Guess what? We do it again but with df_gym by their joint 'gym_id'.

```python
df = pd.merge(pd.merge(df_checkin,pd.merge(df_user,df_sub,on=['subscription_plan']),on=['user_id']),df_gym,on=['gym_id'])
```
### Datetime conversion and new colums for future analysis
I converted all datetime columns to have the same standart to exclude any future problems.
It all was done with pandas to_datetime() function.
```python
df['checkin_time'] = pd.to_datetime(df['checkin_time'])
df['checkout_time'] = pd.to_datetime(df['checkout_time'])
df['sign_up_date'] = pd.to_datetime(df['sign_up_date'])
```
To analyze data more efficient new columns are created.For these columns we calculate time spent in minutes.Then we took hour,day,month from checkin_time column.For it I used number of dt functions such as hour,day_name(),month_name()
```python
df['time_spent_min']=((df['checkout_time']-df['checkin_time']).dt.total_seconds()/60).astype(int)
df['hour_of_day']=df['checkin_time'].dt.hour
df['day_of_week']=df['checkin_time'].dt.day_name()
df['month_of_year']=df['checkin_time'].dt.month_name()
```




