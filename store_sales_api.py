from json.encoder import INFINITY
from fastapi import FastAPI
from pydantic import BaseModel

import pickle
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from typing import List, Union

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
import uvicorn

app = FastAPI()

# Cargando el modelo:
model_sales = pickle.load(open('src/model.pkl', 'rb'))

#cargando scaler
scaler_model = pickle.load(open('src/scaler_model.pkl', 'rb'))

#cargando encoder
encoder_model = pickle.load(open('src/encoder.pkl', 'rb'))


class Input(BaseModel):
    Store: int
    DayOfWeek: int
    Promo: int
    StateHoliday: str
    SchoolHoliday: int
    StoreType: str
    Assortment: str
    CompetitionDistance: float  
    CompetitionOpen: float
    Day : int
    Month: int
    Year: int
    WeekOfYear: int
    Promo2: int
    Promo2Open: float
    IsPromo2Month: int
          
class Output(BaseModel):
    Store: int
    Sales: float           
        
@app.post('/sales-estimate', response_model=Output, status_code=201)
async def generate_sales_estimate(input: Input):
    print('Nuevo request para predecir las ventas de una tienda:', input) 
    
    
    input_values = [input.Store,
                    input.DayOfWeek,
                    input.Promo,
                    input.StateHoliday,
                    input.SchoolHoliday,
                    input.StoreType,
                    input.Assortment,
                    input.CompetitionDistance,
                    input.CompetitionOpen,
                    input.Day,
                    input.Month,
                    input.Year,
                    input.WeekOfYear,
                    input.Promo2,
                    input.Promo2Open,
                    input.IsPromo2Month]
    
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
    
    preds = np.round(preds,3)
    
    
    return  Output(Store =input.Store, Sales = preds)


if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0", port = 3000,debug =True)