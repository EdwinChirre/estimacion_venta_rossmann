from lib2to3.pgen2.pgen import DFAState
import pickle
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from typing import List, Union

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

#cargando base:

# Cargando el modelo:
model_sales = pickle.load(open('src/model.pkl', 'rb'))

#cargando scaler
scaler_model = pickle.load(open('src/scaler_model.pkl', 'rb'))

#cargando encoder
encoder_model = pickle.load(open('src/encoder.pkl', 'rb'))


#def predict_sales(input_values: List[float]):
    
def predict(input_values: List[Union[int, float,str]]):
    # Creando un numpy array bidimensional
    # Un numpy array es un contenedor eficiente en memoria que permite realizar operaciones numéricas rápidas
    features = [np.array(input_values)]
    
    # Creando un dataframe a partir del array bidimensional
    features_df = pd.DataFrame(features)
    
    input_cols = ['Store', 'DayOfWeek', 'Promo', 'StateHoliday', 'SchoolHoliday', 
              'StoreType', 'Assortment', 'CompetitionDistance', 'CompetitionOpen', 
              'Day', 'Month', 'Year', 'WeekOfYear',  'Promo2', 
              'Promo2Open', 'IsPromo2Month']
    
    
    
    numeric_cols = ['Store', 'Promo', 'SchoolHoliday', 
              'CompetitionDistance', 'CompetitionOpen', 'Promo2', 'Promo2Open', 'IsPromo2Month',
              'Day', 'Month', 'Year', 'WeekOfYear']
    
    categorical_cols = ['DayOfWeek', 'StateHoliday', 'StoreType', 'Assortment']
    
    
    
    features_df.columns = input_cols
    
    
    max_distance = 75860

    features_df['CompetitionDistance'].fillna(max_distance, inplace=True)
 
    features_df[numeric_cols] = scaler_model.transform(features_df[numeric_cols])
    
    features_df['DayOfWeek'] = features_df['DayOfWeek'].astype(int)

    encoded_cols = list(encoder_model.get_feature_names_out(categorical_cols))
    features_df[encoded_cols] = encoder_model.transform(features_df[categorical_cols])
    
    var_final = ['Store', 'Promo', 'SchoolHoliday', 'CompetitionDistance',
       'CompetitionOpen', 'Promo2', 'Promo2Open', 'IsPromo2Month', 'Day',
       'Month', 'Year', 'WeekOfYear', 'DayOfWeek_1', 'DayOfWeek_2',
       'DayOfWeek_3', 'DayOfWeek_4', 'DayOfWeek_5', 'DayOfWeek_6',
       'DayOfWeek_7', 'StateHoliday_0', 'StateHoliday_a', 'StateHoliday_b',
       'StateHoliday_c', 'StoreType_a', 'StoreType_b', 'StoreType_c',
       'StoreType_d', 'Assortment_a', 'Assortment_b', 'Assortment_c']
    
    preds = model_sales.predict(features_df[var_final])
    
    #preds = np.round(preds,2)
    
    print('La venta estimada es: ', preds)
    #print(features_df.columns)
    # print(features_df['DayOfWeek'])
    # print(features_df[['Store', 'Promo', 'SchoolHoliday', 'CompetitionDistance','CompetitionOpen', 'Promo2']])
    # print(features_df[['Promo2Open', 'IsPromo2Month', 'Day',
    #    'Month', 'Year', 'WeekOfYear', 'DayOfWeek_1.0', 'DayOfWeek_2.0']])
    # print(features_df[['DayOfWeek_3.0', 'DayOfWeek_4.0', 'DayOfWeek_5.0', 'DayOfWeek_6.0',
    #    'DayOfWeek_7.0', 'StateHoliday_0', 'StateHoliday_a', 'StateHoliday_b']])
    # print(features_df[['StateHoliday_c', 'StoreType_a', 'StoreType_b', 'StoreType_c',
    #    'StoreType_d', 'Assortment_a', 'Assortment_b', 'Assortment_c']])
    
    
    return preds
  
if __name__ == '__main__':
    venta1 = (1,5,1,'0',1,'c','a',1270.0,82.0,31,7,2015,31,0,0.000000,0) #5453.167
    venta2 = (2,5,1,'0',1,'a','a',570.0,92.0,31,7,2015,31,1,64.131148,1) #6124.113
    venta3 = (3,5,1,'0',1,'a','a',14130.0,103.0,31,7,2015,31,1,51.901639,1) #8411.625
    
    predict(venta1)
    predict(venta2)
    predict(venta3)



