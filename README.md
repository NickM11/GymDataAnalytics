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

// Edit in near future
## Data cleaning
This part describes the process of data cleaning in this project.
### Getting list of unique facilities
There were unnecessery values I wanted to remove.There were duplicates and some of them anyway should have been edited in future for consistency reasons.
```bash

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


