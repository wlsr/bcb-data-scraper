import pandas as pd
import os
from pandasgui import show
from datetime import datetime

names_column = ['pais','unidad monetaria','moneda','tipo cambio bs','tipo cambio M.E.']

file_name = '5-1-2024.ods'
# Ruta del archivo ODS 
file_path = f"data/{file_name}"

# Extraer la fecha
date_str = os.path.splitext(file_name)[0]  # Eliminar la extensión
#day, month, year = date_str.split('-')  # Dividir por el separador '-'
df_date = datetime.strptime(date_str, '%d-%m-%Y').date()
# Leer el archivo 
df = pd.read_excel(file_path, engine='odf', names= names_column)
df['date'] = df_date

# Eliminar filas con valores nulos en 'unidad monetaria'
df = df.dropna(subset=['unidad monetaria'])

# Eliminar la primera fila
df = df.iloc[1:].reset_index(drop=True)

# Filtrar para obtener metales
raw_metales = df[(df['pais'] == 'ORO') | (df['pais'] == 'PLATA')]
df_metales = raw_metales.copy()
df_metales = df_metales.rename(columns={'pais': 'metal'}).reset_index(drop=True)

# Eliminar los metales del DataFrame original
df = df.drop(raw_metales.index)

# Limitar df a las primeras 47 filas
df = df.iloc[:47].reset_index(drop=True)

show(df)
#show(df_metales)
