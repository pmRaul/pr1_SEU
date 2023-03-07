import streamlit as st
import folium
import plotly.express as px
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from streamlit_folium import folium_static

# Inicializar la conexión con Firestore
cred = credentials.Certificate('./baseDatosCredenciales.json')
initialize_app(cred)
db = firestore.client()

# Obtener los datos de las caminatas
caminatas_ref = db.collection('TodoData')
caminatas = caminatas_ref.get()

datos = []

# Añadir el campo de identificador único a cada ubicación
for caminata in caminatas:
    caminata_ = caminata.to_dict()
    caminata_['datos'] = []
    datos.append(caminata_)

# Obtener los datos de las ubicaciones
ubicaciones_ref = db.collection('LocalizacionData')
ubicaciones = ubicaciones_ref.get()

# Añadir el campo de identificador único a cada ubicación
for ubicacion in ubicaciones:
    ubicacion_temp = ubicacion.to_dict()
    for dato in datos:
        if dato['id'] == ubicacion_temp['id']:
            dato['datos'].append(ubicacion_temp)

# Mostrar los datos en Streamlit
st.title('Datos de las caminatas')

# Crear un desplegable para seleccionar cada caminata
caminata_seleccionada = st.selectbox('Selecciona una caminata:', [dato["id"] for dato in datos])

# Encontrar la caminata seleccionada
for dato in datos:
    if dato['id'] == caminata_seleccionada:
        st.subheader(f'Caminata {dato["id"]}')
        st.write(f'Duración: {dato["duracion"]}')
        st.write(f'Fecha de inicio: {dato["fechaInicial"]}')
        st.write(f'Fecha de finalización: {dato["fechaFinal"]}')
        st.write(f'Número de pasos: {dato["numPasos"]}')
        st.write(f'Persona: {dato["persona"]}')
        st.write('Ubicaciones:')
        m = folium.Map(location=[dato['datos'][0]['coords']['latitude'], dato['datos'][0]['coords']['longitude']], zoom_start=15)
        velocidades = []
        alturas = []
        for ubicacion in dato['datos']:
            folium.Marker([ubicacion["coords"]["latitude"], ubicacion["coords"]["longitude"]], popup=f'Fecha: {ubicacion["fecha"]}', tooltip=f'Latitud: {ubicacion["coords"]["latitude"]}, Longitud: {ubicacion["coords"]["longitude"]}').add_to(m)
            velocidades.append(ubicacion["coords"]["speed"])
            alturas.append(ubicacion["coords"]["altitude"])
        folium_static(m)
        
        # Mostrar la gráfica de velocidades
        st.subheader('Gráfica de Velocidades')
        st.line_chart(velocidades)
        
        # Mostrar la gráfica de alturas
        st.subheader('Gráfica de Alturas')
        st.line_chart(alturas)
