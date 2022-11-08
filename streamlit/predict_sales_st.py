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
                                ) -> float:

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
    
    if response.status_code == 201:       
        return response.json().get('Sales')
    else:
        response.raise_for_status()
               
        
header_container = st.container()



with header_container:


    html_temp = """
    <div style="background-color:#3E6D9C ;padding:10px">
    <h2 style="color:white;text-align:center;">
    Formulario de Estimación de ventas ML App </h2>
    </div>
    """
    
    st.markdown(html_temp, unsafe_allow_html=True)
    
    st.write('Llene el siguiente formulario para calcular la venta estimada de su tienda')

    
with st.form(key='sales-estimate-form'):
    col1, col2 = st.columns(2)
    
    Store = col1.text_input(label='Id tienda:')
    #DayOfWeek = col1.slider(label='Día de la semana:', min_value=1, max_value=7)
    DayOfWeek = col1.selectbox('Día de la semana:', [1,2,3,4,5,6,7])
    #Promo = col1.slider(label='Tiene promoción hoy?:', min_value=0, max_value=1)
    Promo = col1.selectbox('Tiene promoción hoy?:', [0,1])
    StateHoliday = col1.selectbox('Feriado estatal:',['a','b','c','0'])
    #SchoolHoliday = col1.slider(label='Le afecta el feriado estatal?:', min_value=0, max_value=1)
    SchoolHoliday = col1.selectbox('Le afecta el feriado estatal?:',[0,1])
    StoreType = col1.selectbox('Tipo de tienda:',['a','b','c','d'])
    Assortment = col1.selectbox('Nivel de surtido:',['a','b','c'])
    CompetitionDistance = col1.text_input(label='Distiancia (m) del competidor más cercano:')
    
    CompetitionOpen = col2.text_input(label='Meses que tiene la competencia:')
    Day = col2.text_input(label='Dia de registro:')
    Month = col2.text_input(label='Mes de registro:')
    Year = col2.text_input(label='Año de registro:')
    WeekOfYear = col2.text_input(label='Numero de semana:')
    #Promo2 = col2.slider(label='Participa de otra promoción?:', min_value=0, max_value=1)
    Promo2 = col2.selectbox('Participa de otra promoción?:', [0,1])
    Promo2Open = col2.text_input(label='Meses desde que la promo2 fue abierta:')
    #IsPromo2Month = col2.slider(label='Hay una promo2 en el mes?:', min_value=0, max_value=1)
    IsPromo2Month = col2.selectbox('Hay una promo2 en el mes?:',  [0,1])
    
    customized_button = st.markdown("""
    <style >
    div.stButton > button:first-child {
        background-color: #578a00;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #00128a;
        color:#ffffff;
        }
    </style>""", unsafe_allow_html=True)
    
    submit = customized_button  # Modified
    
    submit = st.form_submit_button('Estimar Venta')
    
    if submit:
        Sales = execute_prediction_request(Store, DayOfWeek, Promo, StateHoliday, 
                                           SchoolHoliday,StoreType, Assortment, CompetitionDistance, 
                                           CompetitionOpen, Day, Month, Year, WeekOfYear,  Promo2, Promo2Open, IsPromo2Month)
        st.success(f'La venta estimada para la tienda {Store} es ${Sales:.2f} USD')
        #Sales
        #st.success(Sales)
    #else:
        #st.error('Oops!! Algo salió mal en la comunicación con el servicio de predicción.')
            
    
    
    