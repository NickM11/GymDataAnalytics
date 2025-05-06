import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

df_checkin = pd.read_csv('checkin_checkout_history_updated.csv')
df_gym = pd.read_csv('gym_locations_data.csv')
df_sub = pd.read_csv('subscription_plans.csv')
df_user = pd.read_csv('users_data.csv')

# print("Check-in Dimensions:",df_checkin.shape)
# print(df_checkin.dtypes)
# print("Gym_loc Dimensions:",df_gym.shape)
# print(df_gym.dtypes)
# print("Subsc Dimensions:",df_sub.shape)
# print(df_sub.dtypes)
# print("User Dimensions:",df_user.shape)
# print(df_user.dtypes)

#Data cleaning

#getting list of unique facilities
flist = sorted(set(df_gym['facilities'].str.split().explode().str.strip()))
print(flist)
flist.remove('Classes')
flist.remove('Classes,')
flist.remove('Court')
flist.remove('Court,')
flist.remove('CrossFit,')
flist.remove('Pool')
flist.remove('Pool,')
flist.remove('Sauna,')
flist.remove('Wall,')
print(flist)

#Create new colun for each facility,checking if the facility is in each row
for f in flist:
    df_gym[f] = df_gym['facilities'].str.contains(f,case=False,na=False)

#Joining all of the data

df = pd.merge(pd.merge(df_checkin,pd.merge(df_user,df_sub,on=['subscription_plan']),on=['user_id']),df_gym,on=['gym_id'])

#Datetime conversion
df['checkin_time'] = pd.to_datetime(df['checkin_time'])
df['checkout_time'] = pd.to_datetime(df['checkout_time'])
df['sign_up_date'] = pd.to_datetime(df['sign_up_date'])


#Creating new columns for future analysis
df['time_spent_min']=((df['checkout_time']-df['checkin_time']).dt.total_seconds()/60).astype(int)
df['hour_of_day']=df['checkin_time'].dt.hour
df['day_of_week']=df['checkin_time'].dt.day_name()
df['month_of_year']=df['checkin_time'].dt.month_name()



#Removing unnecessary columns
df = df.drop(['user_id','gym_id','checkout_time','first_name','last_name','gender','birthdate','features','facilities','location'],axis=1)

# print(df.dtypes)

#Creating a conditional age column
conditions=[
    (df['age']<25),
    (df['age']>=25) & (df['age']<35),
    (df['age']>=35) & (df['age']<45),
    (df['age']>=45) & (df['age']<55),
    (df['age']>=55)
]
choices = ['18-24','25-34','35-44','45-54','55+']

#this line will create a conditional column using my previously defined conditions,and their corresponding choice outcomes
df['Age_Bracket'] = np.select(conditions,choices,default='0')

#Fix for consistency
new_cols = {'Basketball':'basketball_court',
            'Climbing':'climbing_wall',
            'CrossFit':'crossfit',
            'Sauna':'sauna',
            'Swimming':'swimming_pool',
            'Yoga':'yoga_classes'
}
df = df.rename(new_cols,axis=1)

#checking for missing values
print(df.isna().sum())
msno.matrix(df)
plt.show()

#Check for duplicates
df = df.loc[~df.duplicated()].reset_index(drop=True).copy()
df.loc[df.duplicated()]

#cleaned data frame visualization
print(df.shape)
print(df.describe())
df.head
