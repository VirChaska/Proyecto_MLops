# <h1 align=center> **Proyecto_MLops** </h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

¡Bienvenido a mi proyecto de Machine Learning Operations (MLOps) sobre la predicción de precios de juegos de Steam!

## Contexto y Rol

En el escenario de Steam, una plataforma de videojuegos internacional, la tarea asignada es crear un modelo de ML capaz de predecir el precio de un videojuego. Sin embargo, se presenta un desafío importante: los datos disponibles se encuentran en un estado deficiente, lo que requiere la realización ágil de tareas de Ingeniería de Datos para preparar los datos y lograr una predicción precisa.

## Propuesta de Trabajo

Mi enfoque para resolver este desafío se divide en varias etapas:

### Transformaciones de Datos

La primera tarea es trabajar en la lectura del dataset con el formato correcto y realizar transformaciones necesarias para preparar los datos con el objetivo de que sean accesibles y que puedan ser utilizados de manera efectiva.
Los pasos que realicé en la etapa de transformación fueron los siguientes:
- En la columana `publisher` cambié los valores *NaN* por "Desconocido".
- Después de realizar un análisis, las columnas `url` y `reviews_url` no serán relevantes para el desarrollo, así que, las eliminé del df.
- Al revisar `tags`, siempre se repiten los géneros y para simplificar el modelo, los eliminé.
- En la columna `app_name` solo hay dos *NaN* y en `tittle` hay 2050 *NaN* y como los registros son los mismos, decidí elimnar `tittle` y cambié los valores faltantes de `app_name` por "Desconocido".
- Eliminé la columna `id` ya que será suficiente trabajar con la `app_name`.
- También cambié los valores NaN por "Desconocido" en la columna `developer`.
- En la columna `price` reemplacé por cero aquellos registros que tenían alguna característica de "free", también reeemplacé por sus valores correspondientes aquellos que estaban en otro formato y eliminé aquellos en el que el precio no era distingingle.
- En la columna `sentiment` realicé algunos cambios, porque los datos no estaban muy bien categorizados; así que, reemplacé con "sin clasificar" los *NaN* y los que no tenían una clasificación exacta.
- También realicé algunos ajustes en la columna `metascore`, como poner en un formato correcto los NaN, ya que habían algunos como "NA", en string.
- La columna `realese_date` lo cambié a tipo *datetime* y creé una nueva columna `year` solo con el año. Luego eliminé la columna `realese_date`.
- Como todas las funciones que piden hacer está en base al año, es mejor eliminar los registros NaN de `year`.
- Convertí las columnas `genres` y `specs` a cadena.
- Finalmente guarde el df en formato parquet por una compresión más eficiente y un uso reducido de espacio.

**Ver mayor detalle en el archivo [ETL.ipynb](ETL.ipynb)**


### Desarrollo de la API

Para hacer que los datos de la empresa estén disponibles, he utilizado el framework FastAPI para crear una API que permita a los usuarios realizar consultas específicas. He creado 6 funciones de endpoint utilizando decoradores `@app.get('/')`, cada una de las cuales proporciona información valiosa:

- def `genero(Año: str)`: Devuelve una lista con los 5 géneros más ofrecidos en un año específico.
- def `juegos(Año: str)`: Devuelve una lista con los juegos lanzados en un año determinado.
- def `specs(Año: str)`: Devuelve una lista con los 5 specs que más se repiten en un año específico.
- def `earlyaccess(Año: str)`: Devuelve la cantidad de juegos lanzados en un año con early access.
- def `sentiment(Año: str)`: Devuelve una lista con la cantidad de registros categorizados con un análisis de sentimiento para un año en particular.
- def `metascore(Año: str)`: Devuelve los 5 juegos con el mayor metascore en un año específico.

### Deployment

He optado por usar la plataforma **Render** para el deployment de la API, lo que me permite hacer que la API sea accesible en línea de manera sencilla y eficiente.

### Análisis Exploratorio de Datos (EDA)

Realicé un análisis exploratorio de datos detallado para comprender las relaciones entre las variables en el dataset. Investigué la presencia de outliers, patrones interesantes, ect. para mejorar mi comprensión de los datos y después de todo ese análisis exploratorio, seleccioné las variables para mi predicción, eligiendo: `año`, `metascore` y `género` para predecir el precio. Usé **One-Hot Encoding** para género, porque es una variable categórica. **Ver mayor detalle en el archivo [EDA.ipynb](EDA.ipynb)**

### Modelo de Predicción

Después de haber completado el análisis exploratorio, es hora de entrenar un modelo de machine learning para predecir los precios de los juegos. Basé mi modelo en características como género, año y metascore. He creado una función de predicción que, al ingresar ciertos parámetros, devuelve el precio y el RMSE (Root Mean Square Error) como resultado de la predicción y que sean accesibles a través de una solicitud GET.
- def `predicción(metascore, año, genero)`: Ingresando estos parámetros se recibirá el precio predicho.

## Enlaces importantes

+ [Deployment](https://mlops-deploy-q54n.onrender.com/docs): El proyecto ha sido implementado en una plataforma en línea mediante el uso de Render, asegurando que la aplicación esté disponible en la web para su acceso y uso.
+ [Video explicativo](): Para que el proyecto esté completo, realicé un video explicando el trabajo realizado.
