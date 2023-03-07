import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

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

for dato in datos:
    st.subheader(f'Caminata {dato["id"]}')
    st.write(f'Duración: {dato["duracion"]}')
    st.write(f'Fecha de inicio: {dato["fechaInicial"]}')
    st.write(f'Fecha de finalización: {dato["fechaFinal"]}')
    st.write(f'Número de pasos: {dato["numPasos"]}')
    st.write(f'Persona: {dato["persona"]}')
    st.write('Ubicaciones:')
    #query = db.collection('LocalizacionData').where('id', '==', dato['id']).order_by('timestamp')
    #ubicaciones = query.get()
    for ubicacion in dato['datos']:
        st.write(f'Fecha: {ubicacion["fecha"]}')
        st.write(f'Latitud: {ubicacion["coords"]["latitude"]}')
        st.write(f'Longitud: {ubicacion["coords"]["longitude"]}')
        st.write(f'Altitud: {ubicacion["coords"]["altitude"]}')
        st.write(f'Precisión: {ubicacion["coords"]["accuracy"]}')
        st.write('---')
