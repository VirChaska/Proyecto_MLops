from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Cargar el archivo Parquet en un DataFrame
df = pd.read_parquet('Proyecto_MLops\steam_games.parquet')

@app.get('/genero/{Año}')
def genero(Año: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['anio'] == Año]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el promeblema, entonces no hay datos disponibles para el año {Año}"}
    
    # Crear una lista con todos los géneros de los juegos filtrados
    generos = [genero_juego for lista_generos in df_filtrado['genero'] for genero_juego in lista_generos]
    
    # Crear una Serie de pandas con la cuenta de géneros repetidos
    cuenta_generos = pd.Series(generos).value_counts()
    
    # Tomar los 5 géneros más repetidos
    generos_top = cuenta_generos.head(5)
    
    # Crear un diccionario con los resultados
    resultado = generos_top.to_dict()
    
    return resultado

@app.get('/juegos/{Año}')
def juegos(Año: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['anio'] == Año]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Año}"}
    
    # Obtener la lista de nombres de juegos lanzados en el año
    nombres_juegos = df_filtrado['nombre_app'].tolist()
    
    # Crear un diccionario con los resultados
    resultado = {"juegos_lanzados": nombres_juegos}
    
    return resultado
@app.get('/specs/{Año}')
def specs(Año: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['anio'] == Año]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Año}"}
    
    # Crear una lista con todas las especificaciones de los juegos filtrados
    especificaciones = [espec for lista_especificaciones in df_filtrado['especificaciones'] if isinstance(lista_especificaciones, list) for espec in lista_especificaciones]
    
    # Crear una Serie de pandas con la cuenta de especificaciones repetidas
    cuenta_especificaciones = pd.Series(especificaciones).value_counts()
    
    # Tomar las 5 especificaciones más repetidas
    especificaciones_top = cuenta_especificaciones.head(5)
    
    # Crear un diccionario con los resultados
    resultado = especificaciones_top.to_dict()
    
    return resultado

@app.get('/earlyacces/{Año}')
def earlyacces(Año: str):
    # Filtrar el DataFrame por el año y que tenga acceso temprano (True)
    df_filtrado = df[(df['anio'] == Año) & (df['acceso_temprano'] == True)]
    
    # Verificar si no hay datos disponibles para el año ingresado
    if df_filtrado.empty:
        return {"error1": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Año}",
                "error2": f"Si estás seguro de que no tienes problemas con el error1, entonces significa que no se lanzaron juegos con acceso temprano en el año {Año}"}
    
    # Obtener la cantidad de juegos con acceso temprano
    cantidad = len(df_filtrado)
    
    return cantidad

@app.get('/sentiment/{Año}')
def sentiment(Año: str):
    # Filtrar el DataFrame por el año proporcionado y donde 'sentimiento' no sea NaN
    df_filtrado = df[(df['anio'] == Año) & (~df['sentimiento'].isna())]

    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Año}"}
    
    # Contar las categorías de sentimiento
    sentimiento_count = df_filtrado['sentimiento'].value_counts()
    
    # Convertir los resultados a un diccionario
    resultado = sentimiento_count.to_dict()
    
    return resultado

@app.get('/metascore/{Año}')
def metascore(Año: str):
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['anio'] == Año]
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Año}"}
    # Ordenar el DataFrame por metascore de forma descendente y seleccionar los primeros 5 juegos
    top_juegos = df_filtrado.nlargest(5, 'puntuación_metascore')
    
    # Crear un diccionario con el nombre del juego como clave y su metascore como valor
    resultado = top_juegos.set_index('nombre_app')['puntuación_metascore'].to_dict()
    
    return resultado