import streamlit as st
import plotly.graph_objs as go
from datos_twelve import obtener_datos
from patrones import detectar_patron_5velas
from patrones import detectar_envolventes, detectar_patron_5velas
from patrones import detectar_patron_5velas, detectar_envolventes




st.set_page_config(page_title="Dashboard Envolventes", layout="wide")
st.title("📊 Detección de Patrones Envolventes")

# Lista de símbolos populares (puedes ajustar según proveedor)
divisas_populares = [
    "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "USD/CAD",
    "AUD/USD", "NZD/USD", "EUR/JPY", "EUR/GBP", "GBP/JPY"
]

symbol = st.selectbox("🌐 Selecciona un par de divisas", divisas_populares)


df = obtener_datos(symbol)
df = detectar_envolventes(df)
df, rectangulos, detalles = detectar_patron_5velas(df)
fig = go.Figure()

# Marcadores en el gráfico
fig.add_trace(go.Scatter(
    x=df[df['prediccion_sexta'] == 'CALL']['time'],
    y=df[df['prediccion_sexta'] == 'CALL']['low'] * 0.993,
    mode='markers',
    marker=dict(symbol='star', size=14, color='green'),
    name='🔼 Predicción CALL'
))

fig.add_trace(go.Scatter(
    x=df[df['prediccion_sexta'] == 'PUT']['time'],
    y=df[df['prediccion_sexta'] == 'PUT']['high'] * 1.007,
    mode='markers',
    marker=dict(symbol='star', size=14, color='red'),
    name='🔽 Predicción PUT'
))




fig.add_trace(go.Candlestick(
    x=df['time'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name="Precio"
))

fig.add_trace(go.Scatter(
    x=df[df['alcista']]['time'],
    y=df[df['alcista']]['low'] * 0.995,
    mode='markers',
    marker=dict(symbol='triangle-up', size=12, color='green'),
    name='Envolvente Alcista'
))

fig.add_trace(go.Scatter(
    x=df[df['bajista']]['time'],
    y=df[df['bajista']]['high'] * 1.005,
    mode='markers',
    marker=dict(symbol='triangle-down', size=12, color='red'),
    name='Envolvente Bajista'
))

fig.update_layout(
    xaxis_title="Tiempo",
    yaxis_title="Precio",
    title="📈 Gráfico con Patrones Envolventes",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📢 Últimas predicciones (vela 6)")

preds = df.dropna(subset=['prediccion_sexta'])[['time', 'prediccion_sexta']].tail(5)
st.table(preds.rename(columns={'time': 'Hora', 'prediccion_sexta': 'Señal'}))

for r in rectangulos:
    fig.add_shape(
        type='rect',
        xref='x', yref='y',
        x0=r['x0'], x1=r['x1'],
        y0=r['y0'], y1=r['y1'],
        fillcolor='rgba(200, 200, 255, 0.2)',
        line=dict(width=0),
        layer='below'
    )
st.subheader("📌 Detalles de patrones detectados")
st.dataframe(detalles.tail(10), use_container_width=True)

# Alertas en la última vela
ultima = df.iloc[-1]
if ultima['alcista']:
    st.success("📈 ¡Patrón envolvente alcista detectado en la última vela!")
elif ultima['bajista']:
    st.error("📉 ¡Patrón envolvente bajista detectado en la última vela!")
else:
    st.info("⏳ Sin patrones en la última vela.")
