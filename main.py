from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Cargar el archivo Parquet en un DataFrame
df = pd.read_parquet('_src/Data/steam_games_transform.parquet')

@app.get('/genero/{Year}')
def genero(Year: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['year'] == Year]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el promeblema, entonces no hay datos disponibles para el año {Year}"}
    
    # Crear una lista con todos los géneros de los juegos filtrados
    generos = [genero_juego for lista_generos in df_filtrado['genres'] for genero_juego in lista_generos]
    
    # Crear una Serie de pandas con la cuenta de géneros repetidos
    cuenta_generos = pd.Series(generos).value_counts()
    
    # Tomar los 5 géneros más repetidos
    generos_top = cuenta_generos.head(5)
    
    # Crear un diccionario con los resultados
    resultado = generos_top.to_dict()
    
    return resultado

@app.get('/juegos/{Year}')
def juegos(Year: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['year'] == Year]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Obtener la lista de nombres de juegos lanzados en el año
    nombres_juegos = df_filtrado['app_name'].tolist()
    
    # Crear un diccionario con los resultados
    resultado = {"juegos_lanzados": nombres_juegos}
    
    return resultado

@app.get('/specs/{Year}')
def specs(Year: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['year'] == Year]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Usar explode para dividir las listas en filas separadas
    df_exploded = df_filtrado.explode('specs')
    
    # Crear una Serie de pandas con la cuenta de especificaciones repetidas
    cuenta_especificaciones = df_exploded['specs'].value_counts()
    
    # Tomar las 5 especificaciones más repetidas
    especificaciones_top = cuenta_especificaciones.head(5)
    
    # Crear un diccionario con los resultados
    resultado = especificaciones_top.to_dict()
    
    return resultado
specs("2008")

@app.get('/earlyacces/{Year}')
#def earlyacces( Año: str ): Cantidad de juegos lanzados en un año con early access
def earlyacces(Year: str):
    # Filtrar el DataFrame por el año y que tenga acceso temprano (True)
    df_filtrado = df[(df['year'] == Year) & (df['early_access'] == True)]
    
    # Verificar si no hay datos disponibles para el año ingresado
    if df_filtrado.empty:
        return {"error1": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}",
                "error2": f"Si estás seguro de que no tienes problemas con el error1, entonces significa que no se lanzaron juegos con acceso temprano en el año {Year}"}
    
    # Obtener la cantidad de juegos con acceso temprano
    cantidad = len(df_filtrado)
    # Crear un diccionario con el resultado
    resultado = {
        "year": Year,
        "early_access_count": cantidad
    }
    
    return resultado

@app.get('/sentiment/{Year}')
#def sentiment( Año: str ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros 
#que se encuentren categorizados con un análisis de sentimiento.
def sentiment(Year: str):
    # Filtrar el DataFrame por el año proporcionado y donde 'sentimiento' no sea NaN
    df_filtrado = df[(df['year'] == Year) & (~df['sentiment'].isna())]

    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Contar las categorías de sentimiento
    sentimiento_count = df_filtrado['sentiment'].value_counts()
    
    # Convertir los resultados a un diccionario
    resultado = sentimiento_count.to_dict()
    
    return resultado

@app.get('/metascore/{Year}')
def metascore(Year: str):
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['year'] == Year]
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado esté en el formato correcto. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    # Ordenar el DataFrame por metascore de forma descendente y seleccionar los primeros 5 juegos
    top_juegos = df_filtrado.nlargest(5, 'metascore')
    
    # Crear un diccionario con el nombre del juego como clave y su metascore como valor
    resultado = top_juegos.set_index('app_name')['metascore'].to_dict()
    
    return resultado
