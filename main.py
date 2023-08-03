from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Cargar el archivo Parquet en un DataFrame
df = pd.read_parquet('_src\Data\steam_games.parquet')

@app.get('/genero/{Year}')
def genero_por_anio(Year: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['anio'] == Year]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Crear una lista con todos los géneros de los juegos filtrados
    generos = [genero_juego for lista_generos in df_filtrado['genero'] for genero_juego in lista_generos]
    
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
    df_filtrado = df[df['anio'] == Year]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Obtener la lista de nombres de juegos lanzados en el año
    nombres_juegos = df_filtrado['nombre_app'].tolist()
    
    # Crear un diccionario con los resultados
    resultado = {"juegos_lanzados": nombres_juegos}
    
    return resultado
@app.get('/specs/{Year}')
def specs(Year: str): 
    # Filtrar el DataFrame por el año proporcionado
    df_filtrado = df[df['anio'] == Year]
    
    # Verificar si hay datos para el año ingresado
    if df_filtrado.empty:
        return {"error": f"Asegúrate de que el año ingresado sea de tipo 'str', por ejemplo: '2000' y no 'dos mil' o 2000. Si ese no es el problema, entonces no hay datos disponibles para el año {Year}"}
    
    # Crear una lista con todas las especificaciones de los juegos filtrados
    especificaciones = [espec for lista_especificaciones in df_filtrado['especificaciones'] if isinstance(lista_especificaciones, list) for espec in lista_especificaciones]
    
    # Crear una Serie de pandas con la cuenta de especificaciones repetidas
    cuenta_especificaciones = pd.Series(especificaciones).value_counts()
    
    # Tomar las 5 especificaciones más repetidas
    especificaciones_top = cuenta_especificaciones.head(5)
    
    # Crear un diccionario con los resultados
    resultado = especificaciones_top.to_dict()
    
    return resultado

