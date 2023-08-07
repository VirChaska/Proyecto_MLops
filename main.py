from fastapi import FastAPI, Query
from enum import Enum
import pickle
import pandas as pd
import numpy as np

app = FastAPI()

df = pd.read_parquet('_src/Data/steam_games_transform.parquet')

@app.get('/genero/{Year}')
def genero(Year: str):
    df_filtrado = df[df['year'] == Year]
    
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Creamos una lista con el total de géneros para ese año
    generos = []
    for lista_generos in df_filtrado['genres']:
        if lista_generos is not None:
            for genero in lista_generos.split(','):
                generos.append(genero.strip())
    
    # Luego creamos una Serie de pandas contando los géneros repetidos
    cuenta_generos = pd.Series(generos).value_counts()

    # Finalmente creamos un diccionario con los 5 géneros más repetidos en el año filtrado
    resultado = cuenta_generos.head(5).to_dict()
    return resultado

@app.get('/juegos/{Year}')
def juegos(Year: str): 
    df_filtrado = df[df['year'] == Year]

    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Con el método tolist obtenemos una lista con el nombre de los juegos para ese año
    nombres_juegos = df_filtrado['app_name'].tolist()
    
    # Finalmente, creamos un diccionario
    resultado = {"juegos_lanzados": nombres_juegos}
    
    return resultado

@app.get('/specs/{Year}')
def specs(Year: str):

    df_filtrado = df[df['year'] == Year]
   
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Creamos una lista con el total de especificaciones para ese año
    total_specs = []
    for lista_specs in df_filtrado['specs']:
        if lista_specs is not None:
            for spec in lista_specs.split(','):
                total_specs.append(spec.strip())
    
    # Luego creamos una Serie de pandas contando las especificaciones repetidas
    cuenta_specs = pd.Series(total_specs).value_counts()

    # Creamos un diccionario con los 5 specs que más se repiten
    resultado = cuenta_specs.head(5).to_dict()
    
    return resultado

@app.get('/earlyacces/{Year}')
def earlyacces(Year: str):

    df_filtrado = df[(df['year'] == Year) & (df['early_access'] == True)]
    
    if df_filtrado.empty:
        return {"error1": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}",
                "error2": f"Si estás seguro de que no tienes problemas con el error1, entonces significa que no se lanzaron juegos con acceso temprano en el año {Year}"}
    
    # Usamos len() para obtener la cantidad de juegos con early access
    cantidad = len(df_filtrado)

    # Finalmente, creamos un diccionario
    resultado = {
        "anio": Year,
        "Cantidad de juegos lanzados": cantidad
    }
    
    return resultado

@app.get('/sentiment/{Year}')
#def sentiment( Año: str ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros 
#que se encuentren categorizados con un análisis de sentimiento.
def sentiment(Year: str):
    #Como tenemos muchos registros sin clasificar, nos aseguramos de que no salga en nuestro resultado
    df_filtrado = df[(df['year'] == Year) & (df['sentiment']!='sin clasificar')]

    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Realizamos un conteo total de las categorías de sentimiento
    sentimiento_total = df_filtrado['sentiment'].value_counts()
    
    # el resultado debe ser un diccionario
    resultado = sentimiento_total.to_dict()
    
    return resultado

@app.get('/metascore/{Year}')
def metascore(Year: str):

    df_filtrado = df[df['year'] == Year]

    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}

    top_juegos = df_filtrado.nlargest(5, 'metascore')[['app_name', 'metascore']]
    
    # finalmente, creamos un diccionario
    resultado = top_juegos.set_index('app_name')['metascore'].to_dict()
    
    return resultado


class GeneroJuego(str, Enum):
    action = "action"
    adventure = "adventure"
    casual = "casual"
    early_access = "early access"
    free_to_play = "free to play"
    indie = "indie"
    massively_multiplayer = "massively multiplayer"
    racing = "racing"
    rpg = "rpg"
    simulation = "simulation"
    sports = "sports"
    strategy = "strategy"
    video_production = "video production"

@app.get("/prediccion/")
def prediccion_precio(metascore: float = Query(None, description="Metascore del juego (ej: 86)"),
                       year: int = Query(None, description="Año de lanzamiento del juego (ej: 2002)"),
                       genero: GeneroJuego = Query(None, description="Género del juego")):
    # Cargamos el modelo
    with open('_src/Data/modelo_final.pkl', 'rb') as archivo_modelo:
        modelo, rmse = pickle.load(archivo_modelo)

    # Listamos todos los géneros y obtenemos sus respectivos índices
    generos = list(GeneroJuego)
    genero_index = generos.index(genero)

    input_dato = np.array([[metascore, year] + [0] * genero_index + [1] + [0] * (len(generos) - genero_index - 1)])

    precio_predicho = modelo.predict(input_dato)

    return {"Precio_predicho": precio_predicho[0], "RMSE": rmse}