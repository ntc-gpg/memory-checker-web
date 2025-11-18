import streamlit as st
import psutil
import time
import plotly.graph_objects as go
import uuid 

st.set_page_config(page_title="Monitor de Memória", layout="wide")

st.title("Monitoramento de Memória")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Relógio de Uso")
    gauge_placeholder = st.empty()

with col2:
    st.subheader("Gráfico de Distribuição")
    donut_placeholder = st.empty()

metrics_placeholder = st.empty()

while True:
    memory = psutil.virtual_memory()
    
    total_gb = memory.total / (1024 ** 3)
    used_gb = memory.used / (1024 ** 3)
    free_gb = memory.available / (1024 ** 3)
    percent = memory.percent
    
    #visual relogio
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Uso (%)"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
        }
    ))
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))

    # grafico circulo
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Usada', 'Livre'],
        values=[used_gb, free_gb],
        hole=.6,
        marker_colors=['#FF4B4B', '#00CC96']
    )])
    fig_donut.update_layout(height=300, showlegend=True, margin=dict(l=20, r=20, t=0, b=0))

    unique_key_gauge = f"gauge_{uuid.uuid4()}"
    unique_key_donut = f"donut_{uuid.uuid4()}"

    gauge_placeholder.plotly_chart(fig_gauge, use_container_width=True, key=unique_key_gauge)
    donut_placeholder.plotly_chart(fig_donut, use_container_width=True, key=unique_key_donut)
    
    with metrics_placeholder.container():
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Ram", f"{total_gb:.2f} GB")
        kpi2.metric("Disponível", f"{free_gb:.2f} GB")
        kpi3.metric("Usada", f"{used_gb:.2f} GB")

    time.sleep(10)