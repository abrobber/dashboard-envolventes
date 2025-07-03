import streamlit as st
import plotly.graph_objs as go
from datos_twelve import obtener_datos
from patrones import detectar_envolventes

st.set_page_config(page_title="Dashboard Envolventes", layout="wide")
st.title("📊 Detección de Patrones Envolventes")

df = obtener_datos()
df = detectar_envolventes(df)

fig = go.Figure()

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

# Alertas en la última vela
ultima = df.iloc[-1]
if ultima['alcista']:
    st.success("📈 ¡Patrón envolvente alcista detectado en la última vela!")
elif ultima['bajista']:
    st.error("📉 ¡Patrón envolvente bajista detectado en la última vela!")
else:
    st.info("⏳ Sin patrones en la última vela.")
