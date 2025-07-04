import requests
import pandas as pd
import yaml

def cargar_configuracion(ruta="config.yaml"):
    with open(ruta, "r") as f:
        return yaml.safe_load(f)

def obtener_datos(symbol):
    config = cargar_configuracion()
    url = (
        f"https://api.twelvedata.com/time_series?"
        f"symbol={symbol}&interval={config['interval']}&outputsize={config['outputsize']}"
        f"&apikey={config['api_key']}&format=JSON"
    )
    resp = requests.get(url)
    data = resp.json().get('values', [])
    df = pd.DataFrame(data)
    df.rename(columns={
        'datetime': 'time',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close'
    }, inplace=True)
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df['time'] = pd.to_datetime(df['time'])
    return df.sort_values('time')
