# Importar librerías
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from geopy.distance import distance
import streamlit as st
import folium

# Obtener la base de datos
cred = credentials.Certificate("./baseDatosCredenciales.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Obtener los datos
def get_data():
    docs = db.collection("caminatas").stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)

# Procesar los datos
def process_data(data):
    data = data.copy() # evitar posibles efectos secundarios en el DataFrame original

    # Convertir fechas a datetime
    for col in ["fechaInicial", "fechaFinal", "fecha"]:
        data[col] = pd.to_datetime(data[col], format="%d de %B de %Y, %H:%M:%S %Z%z")

    # Calcular la distancia en cada punto
    coords = [(row["coords"]["latitude"], row["coords"]["longitude"]) for _, row in data.iterrows()]
    distances = [0] + [distance(coords[i], coords[i+1]).meters for i in range(len(coords)-1)]
    data["distancia"] = distances

    # Agregar columnas de latitud y longitud inicial y final
    data["latInicial"] = data.iloc[0]["coords"]["latitude"]
    data["lonInicial"] = data.iloc[0]["coords"]["longitude"]
    data["latFinal"] = data.iloc[-1]["coords"]["latitude"]
    data["lonFinal"] = data.iloc[-1]["coords"]["longitude"]

    # Calcular la duración en minutos
    data["duracion"] = (data["fechaFinal"] - data["fechaInicial"]).dt.total_seconds() / 60

    return data

# Crear una aplicación Streamlit que muestre los datos procesados
def show_data(data):
    # Mostrar la información general
    st.header("Caminata de {} ({})".format(data.iloc[0]["persona"], data.iloc[0]["fechaInicial"].strftime("%d/%m/%Y")))
    st.subheader("Duración: {} minutos".format(int(data.iloc[0]["duracion"])))
    st.subheader("Número de pasos: {}".format(data.iloc[0]["numPasos"]))

    # Mostrar el mapa
    m = folium.Map(location=[data.iloc[0]["latInicial"], data.iloc[0]["lonInicial"]], zoom_start=16)
    for _, row in data.iterrows():
        folium.Marker([row["coords"]["latitude"], row["coords"]["longitude"]], popup=row["fecha"].strftime("%H:%M:%S")).add_to(m)
    folium.PolyLine([[row["coords"]["latitude"], row["coords"]["longitude"]] for _, row in data.iterrows()], color="red").add_to(m)
    folium.Marker([data.iloc[0]["latInicial"], data.iloc[0]["lonInicial"]], popup="Inicio").add_to(m)
    folium.Marker([data.iloc[-1]["latFinal"], data.iloc[-1]["lonFinal"]], popup="Fin").add_to(m)
    st.markdown(folium.Markdown(m._repr_html_()), unsafe_allow_html=True)

    # Mostrar la tabla de datos
    st.write(data[["fecha", "coords", "distancia"]])

# Ejecutar la aplicación
if __name__ == "__main__":
    data = get_data()
    data = process_data(data)
