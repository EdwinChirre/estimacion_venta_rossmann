import streamlit as st
import requests
import json

API_URLBASE = "https://sales-estimate-container-service.e5tasnbtgnsga.us-east-1.cs.amazonlightsail.com"

def execute_prediction_request(Store: int,
    DayOfWeek: int,
    Promo: int,
    StateHoliday: str,
    SchoolHoliday: int,
    StoreType: str,
    Assortment: str,
    CompetitionDistance: float , 
    CompetitionOpen: float,
    Day : int,
    Month: int,
    Year: int,
    WeekOfYear: int,
    Promo2: int,
    Promo2Open: float,
    IsPromo2Month: int
                                ):# -> float:

    payload = {
        'Store': Store,
        'DayOfWeek': DayOfWeek,
        'Promo': Promo,
        'StateHoliday': StateHoliday,
        'SchoolHoliday': SchoolHoliday,
        'StoreType': StoreType,
        'Assortment': Assortment,
        'CompetitionDistance': CompetitionDistance,
        'CompetitionOpen': CompetitionOpen,
        'Day': Day,
        'Month': Month,
        'Year': Year,
        'WeekOfYear': WeekOfYear,
        'Promo2': Promo2,
        'Promo2Open': Promo2Open,
        'IsPromo2Month': IsPromo2Month
        
    }
    
    response = requests.post(API_URLBASE + '/sales-estimate', data=json.dumps(payload))
    
    #return response
    
    if response.status_code == 201:       
        return response.json().get('Sales')
    else:
        response.raise_for_status()
        
Sales = execute_prediction_request(1,5,1,'0',1,'c','a',1270.0,82.0,31,7,2015,31,0,0.000000,0)   
print(Sales)     