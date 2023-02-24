# Título del proyecto

Este proyecto es una aplicación web que muestra los datos recogidos de un dispositivo móvil durante una caminata. La aplicación permite visualizar la duración de la caminata, el número de pasos dados, y la ruta recorrida en un mapa interactivo.

## Tecnologías utilizadas

La aplicación está desarrollada en Python utilizando las siguientes tecnologías:

- Firebase: para almacenar los datos de la caminata.
- Pandas: para procesar los datos de la caminata.
- Streamlit: para crear la interfaz de usuario.
- Folium: para crear el mapa interactivo.

## Requerimientos

Antes de poder ejecutar la aplicación es necesario tener instalado lo siguiente:

- Python 3.7 o superior
- Las bibliotecas `firebase-admin`, `pandas`, `streamlit`, y `folium`. Puedes instalarlas ejecutando el siguiente comando:

```bash
pip install firebase-admin pandas streamlit folium

## Cómo ejecutar la aplicación

1. Descarga el repositorio en tu ordenador.
2, Crea un proyecto Firebase en la consola de Firebase y descarga las credenciales de tu proyecto. Para más información, consulta la documentación de Firebase.
3. Añade las credenciales de tu proyecto Firebase al archivo firebase_config.json.
4. Ejecuta el siguiente comando para iniciar la aplicación:

```bash
streamlit run app.py

5. Abre tu navegador web y ve a la dirección http://localhost:8501

## Cómo contribuir
Si deseas contribuir a este proyecto, ¡estamos encantados de recibir tus sugerencias y comentarios! Para hacerlo, por favor sigue los siguientes pasos:

1. Realiza un fork del repositorio.
2. Crea una rama con el nombre de tu nueva característica (git checkout -b nueva-caracteristica).
3. Realiza tus cambios y haz un commit (git commit -am "Agrega nueva característica").
4. Envía tus cambios a tu repositorio remoto (git push origin nueva-caracteristica).
5. Crea un pull request en este repositorio para que podamos revisar tus cambios y fusionarlos con la rama principal.