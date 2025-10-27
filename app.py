import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXDVn23Cp8Obiw7FQrebnVGgqza6dw5RIP9EKfVhvfjd2Psh0BFtU9H_p2AMzjKkU5-YNEXaJqf5bF/pub?gid=1542986716&single=true&output=csv"

albergues = pd.read_csv(url)
albergues.columns = albergues.columns.str.strip().str.lower()
albergues['latitud'] = pd.to_numeric(albergues['latitud'], errors='coerce')
albergues['longitud'] = pd.to_numeric(albergues['longitud'], errors='coerce')
albergues = albergues.dropna(subset=['latitud','longitud'])

lat_mean = albergues['latitud'].mean()
lon_mean = albergues['longitud'].mean()

st.set_page_config(page_title="Red de Albergues México", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');
body {background-color: #1e1e1e; color: white; font-family: 'Montserrat', sans-serif;}
h1 {color: #00FFCC; font-weight: 600;}
p {color: #ccc;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color:#00FFCC;'>Filtros</h2>", unsafe_allow_html=True)
entidades = sorted(albergues['entidad federativa'].unique())
entidad_sel = st.sidebar.multiselect("Selecciona por estado:", entidades)

if entidad_sel:
    municipios = sorted(albergues[albergues['entidad federativa'].isin(entidad_sel)]['municipio'].unique())
else:
    municipios = sorted(albergues['municipio'].unique())
municipio_sel = st.sidebar.multiselect("Selecciona por municipio:", municipios)
busqueda = st.sidebar.text_input("🔍 Buscar por nombre de albergue")

df = albergues.copy()
if entidad_sel: df = df[df['entidad federativa'].isin(entidad_sel)]
if municipio_sel: df = df[df['municipio'].isin(municipio_sel)]
if busqueda: df = df[df['nombre albergue'].str.contains(busqueda, case=False, na=False)]

m = folium.Map(location=[lat_mean, lon_mean], zoom_start=6, tiles='CartoDB Dark_Matter', width='100%', height=700)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={row['latitud']},{row['longitud']}"
    popup_html = f"""<div style="font-size:13px; font-family:Montserrat;">
<b style="color:#00FFCC;">{row['nombre albergue']}</b><br>
{row['entidad federativa']} - {row['municipio']}<br>
<b>Dirección:</b> {row.get('dirección', 'N/A')}<br>
<a href="{google_maps_url}" target="_blank" style="display:inline-block;background-color:#00796B;color:white;padding:6px 10px;text-decoration:none;border-radius:5px;font-size:12px;">📍 ¿Cómo llegar?</a>
</div>"""
    folium.CircleMarker(location=[row['latitud'], row['longitud']], radius=7, color='#00FFCC', fill=True, fill_color='#00FFCC', fill_opacity=0.9, popup=folium.Popup(popup_html, max_width=300)).add_to(marker_cluster)

st_folium(m, width=1000, height=700)
st.markdown("""<div style="text-align:center; margin-top:15px; font-size:13px; color:#aaa;">
<hr style="border:none; border-top:1px solid #444; width:70%; margin:10px auto;">
<p><b>Fuentes:</b><br>
<a href='https://www.gob.mx' target='_blank' style='color:#00FFCC;'>Gobierno de México</a> |
<a href='https://www.facebook.com/CNPCmx/' target='_blank' style='color:#00FFCC;'>Coordinación Nacional de Protección Civil</a> |
<a href='https://www.gob.mx/reporteporlluvias/nav-zonas' target='_blank' style='color:#00FFCC;'>Reporte lluvias</a>
</p></div>""", unsafe_allow_html=True)
