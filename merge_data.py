import pandas as pd
import os
import numpy as np
from pandasgui import show
from datetime import datetime
from connection import * 

numeric = ['exchange_rate_bs', 'exchange_rate_me']

def process_file(file_path, name_column):
    
    # Extraer la fecha del nombre del archivo
    file_name = os.path.basename(file_path)
    date_str = os.path.splitext(file_name)[0]  # Eliminar la extensión
    df_date = datetime.strptime(date_str, '%d-%m-%Y').date()
    
    # Leer el archivo ODS
    df = pd.read_excel(file_path, engine='odf', skiprows=10, names=name_column, usecols='A:E')
    
     # Inicializar el DataFrame de metales
    df_metales = pd.DataFrame()
    
    if df.shape[0] < 15:
        return None, None
        
    # Reemplazar espacios en blanco y cadenas vacías con NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
    # Añadir la fecha
    df['date'] = df_date
    
    # Eliminar filas con valores nulos en 'unidad monetaria'
    df = df.dropna(subset=['monetary_unit']) 
    
    # Eliminar filas donde ambos tipos de cambio son NaN
    df = df.dropna(subset=['country','exchange_rate_bs', 'exchange_rate_me'], how='all')
    
    # Eliminar las comas de las columnas especificadas
    df[numeric] = df[numeric].replace({',': ''}, regex=True)

    # Convertir las columnas especificadas en la lista 'numeric' a numérico, forzando errores a NaN
    df[numeric] = df[numeric].apply(pd.to_numeric, errors='coerce')

    # Filtrar para obtener metales
    raw_metales = df[(df['country'] == 'ORO') | (df['country'] == 'PLATA')]
    df_metales = raw_metales.copy()

    # Eliminar los metales del DataFrame original
    df = df.drop(raw_metales.index)

    # Extraer currency
    index_to_keep = df[(df['monetary_unit'] == 'UNIDAD DE FOMENTO DE VIVIENDA') | (df['currency'] == 'Bs/UFV')].index
    if not index_to_keep.empty:
        df = df.loc[:index_to_keep[0]]
    
    return df, df_metales

    
def merge_data(directory_path):
    names_column = ['country', 'monetary_unit', 'currency', 'exchange_rate_bs', 'exchange_rate_me']
    all_df = pd.DataFrame()
    all_df_metales = pd.DataFrame()

    # Procesar cada archivo .ods en el directorio
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.ods'):
            file_path = os.path.join(directory_path, file_name)
            df, df_metales = process_file(file_path, names_column)
            
            # Si el resultado es None, pasar al siguiente archivo
            if df is None or df_metales is None:
                continue

            # Concatenar los resultados con los DataFrames globales
            all_df = pd.concat([all_df, df], ignore_index=True)
            all_df_metales = pd.concat([all_df_metales, df_metales], ignore_index=True)
            
    # Restablecer el índice de all_df_metales
    all_df_metales.reset_index(drop=True, inplace=True)

    if 'exchange_rate_bs' in all_df_metales.columns:
        all_df_metales['exchange_rate_me'] = all_df_metales['exchange_rate_bs']
        all_df_metales = all_df_metales.drop(columns=['exchange_rate_bs'])
    else:
        print("La columna 'exchange_rate_bs' no existe en all_df_metales.")
    
    all_df_metales.rename(columns={'country':'metal'}, inplace=True)
    
    # Mostrar los DataFrames resultantes
    print(all_df.shape)
    print(all_df_metales.shape)
    
    # guardar en un csv for the tests
    df.to_csv('data/raw_exchange_rates.csv', index=False)
    
    # Puedes devolver los DataFrames si lo necesitas para otros fines
    return all_df, all_df_metales

# Ejecutar la función para procesar los archivos en la carpeta 'data'
directory_path = 'data'  # Asegúrate de que esta carpeta exista
all_df, all_df_metales = merge_data(directory_path)

load_data_db(all_df, 'raw_exchange_rates')
load_data_db(all_df_metales, 'raw_metals')