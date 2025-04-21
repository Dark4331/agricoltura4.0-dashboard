import pandas as pd
import numpy as np
import requests

def load_clean_data():
    """Carica e pulisce dati da fonti eterogenee."""
    # Caricamento dati aziendali
    df = pd.read_excel("data/raccolti.xlsx")
    
    # Pulizia: rimozione duplicati e valori anomali
    df = df.drop_duplicates(subset=['data', 'campo', 'coltura'])
    df = df[(df['resa_kg'] > 0) & (df['resa_kg'] < 15000)]  # Filtra outlier
    
    # Caricamento dati meteo via API
    weather_data = fetch_weather_data("API_KEY_OPENWEATHER")
    df = pd.merge(df, weather_data, on='data', how='left')
    
    # Conversione unità di misura
    df['ettari'] = df['acri'] * 0.404686  # Acri → Ettari
    
    return df

def fetch_weather_data(api_key: str):
    """Recupera dati storici meteo da OpenWeatherMap."""
    response = requests.get(
        f"https://api.openweathermap.org/data/3.0/onecall/timemachine?"
        f"lat=45.46&lon=9.18&dt=1641043200&appid={api_key}"
    )
    return pd.json_normalize(response.json()['data'])
