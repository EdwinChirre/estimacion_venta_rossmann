from lib2to3.pgen2.pgen import DFAState
import pickle
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from typing import List

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

#cargando base:

ross_df = pd.read_csv('data/train.csv',low_memory=False)
store_df = pd.read_csv('data/store.csv')
merged_df = ross_df.merge(store_df, how='left', on='Store')
df = merged_df[merged_df["Open"] == 1].copy()


# Cargando el modelo:
model_sales = pickle.load(open('src/model.pkl', 'rb'))

#cargando scaler
scaler = pickle.load(open('src/scaler_model.pkl', 'rb'))

#cargando encoder
encoder = pickle.load(open('src/encoder.pkl', 'rb'))


#funciones
def split_date(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df.Date.dt.year
    df['Month'] = df.Date.dt.month
    df['Day'] = df.Date.dt.day
    df['WeekOfYear'] = df.Date.dt.isocalendar().week
    
def comp_months(df):
    df['CompetitionOpen'] = 12 * (df.Year - df.CompetitionOpenSinceYear) + (df.Month - df.CompetitionOpenSinceMonth)
    df['CompetitionOpen'] = df['CompetitionOpen'].map(lambda x: 0 if x < 0 else x).fillna(0)
    
def check_promo_month(row):
    month2str = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',              
                 7:'Jul', 8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}
    try:
        months = (row['PromoInterval'] or '').split(',')
        if row['Promo2Open'] and month2str[row['Month']] in months:
            return 1
        else:
            return 0
    except Exception:
        return 0

def promo_cols(df):
    # Months since Promo2 was open
    df['Promo2Open'] = 12 * (df.Year - df.Promo2SinceYear) +  (df.WeekOfYear - df.Promo2SinceWeek)*7/30.5
    df['Promo2Open'] = df['Promo2Open'].map(lambda x: 0 if x < 0 else x).fillna(0) * df['Promo2']
    # Whether a new round of promotions was started in the current month
    df['IsPromo2Month'] = df.apply(check_promo_month, axis=1) * df['Promo2']
    
#variables:
input_cols = ['Store', 'DayOfWeek', 'Promo', 'StateHoliday', 'SchoolHoliday', 
              'StoreType', 'Assortment', 'CompetitionDistance', 'CompetitionOpen', 
              'Day', 'Month', 'Year', 'WeekOfYear',  'Promo2', 
              'Promo2Open', 'IsPromo2Month','Sales']


numeric_cols = ['Store', 'Promo', 'SchoolHoliday', 
              'CompetitionDistance', 'CompetitionOpen', 'Promo2', 'Promo2Open', 'IsPromo2Month',
              'Day', 'Month', 'Year', 'WeekOfYear']
categorical_cols = ['DayOfWeek', 'StateHoliday', 'StoreType', 'Assortment']


#def predict_sales(input_values: List[float]):
    
    
split_date(df)
comp_months(df)
promo_cols(df)

max_distance = 75860

df['CompetitionDistance'].fillna(max_distance, inplace=True)


df = df[input_cols]#.reset_index(drop=True)       

df[numeric_cols] = scaler.transform(df[numeric_cols])

encoded_cols = list(encoder.get_feature_names_out(categorical_cols))
df[encoded_cols] = encoder.transform(df[categorical_cols])


print(df.head(3))
print(df.columns)
