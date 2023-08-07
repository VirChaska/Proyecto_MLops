<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **Proyecto_MLops** </h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

¡Bienvenido a mi proyecto de Machine Learning Operations (MLOps) sobre la predicción de precios de juegos de Steam!

## Contexto y Rol

En el escenario de Steam, una plataforma de videojuegos internacional, la tarea asignada es crear un modelo de ML capaz de predecir el precio de un videojuego. Sin embargo, se presenta un desafío importante: los datos disponibles se encuentran en un estado deficiente, lo que requiere la realización ágil de tareas de Ingeniería de Datos para preparar los datos y lograr una predicción precisa.

## Propuesta de Trabajo

Mi enfoque para resolver este desafío se divide en varias etapas clave:

### Transformaciones de Datos

La primera tarea es trabajar en la lectura del dataset con el formato correcto y realizar transformaciones necesarias para preparar los datos con el objetivo de que sean accesibles y puedan ser utilizados de manera efectiva.

### Desarrollo de la API

Para hacer que los datos de la empresa estén disponibles, he utilizado el framework FastAPI para crear una API que permita a los usuarios realizar consultas específicas. He creado 6 funciones de endpoint utilizando decoradores `@app.get('/')`, cada una de las cuales proporciona información valiosa:

- `genero(Año: str)`: Devuelve una lista con los 5 géneros más ofrecidos en un año específico.
- `juegos(Año: str)`: Devuelve una lista con los juegos lanzados en un año determinado.
- `specs(Año: str)`: Devuelve una lista con los 5 specs que más se repiten en un año específico.
- `earlyaccess(Año: str)`: Devuelve la cantidad de juegos lanzados en un año con early access.
- `sentiment(Año: str)`: Devuelve una lista con la cantidad de registros categorizados con un análisis de sentimiento para un año en particular.
- `metascore(Año: str)`: Devuelve los 5 juegos con el mayor metascore en un año específico.

### Deployment

He optado por usar la plataforma Render para el deployment de la API, lo que me permite hacer que la API sea accesible en línea de manera sencilla y eficiente.

### Análisis Exploratorio de Datos (EDA)

Realicé un análisis exploratorio de datos detallado para comprender las relaciones entre las variables en el dataset. Investigué la presencia de outliers, patrones interesantes, ect. para mejorar mi comprensión de los datos.

### Modelo de Predicción

Después de haber completado el análisis exploratorio, es hora de entrenar un modelo de machine learning para predecir los precios de los juegos. Basé mi modelo en características como género, año y metascore. He creado una función de predicción que, al ingresar ciertos parámetros, devuelve el precio y el RMSE (Root Mean Square Error) como resultado de la predicción y que sean accesibles a través de una solicitud GET.

## Enlaces importantes

+ [Deployment](https://mlops-deploy-q54n.onrender.com/docs): El proyecto ha sido implementado en una plataforma en línea mediante el uso de Render, asegurando que la aplicación esté disponible en la web para su acceso y uso.
+ [Video explicativo](): Para que el proyecto esté completo, realicé un video explicando el trabajo realizado.
