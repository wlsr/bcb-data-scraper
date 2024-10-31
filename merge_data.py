import pandas as pd
import os
import numpy as np
from pandasgui import show
from datetime import datetime
from connection import * 

numeric = ['exchange_rate_bs', 'exchange_rate_me']

def process_file(file_path, name_column):
    
    # Extract date from file name 
    file_name = os.path.basename(file_path)
    date_str = os.path.splitext(file_name)[0]  # remove extension
    df_date = datetime.strptime(date_str, '%d-%m-%Y').date()
    
    # Read the file
    df = pd.read_excel(file_path, engine='odf', skiprows=10, names=name_column, usecols='A:E')
    
     # Initialize the df_metals DataFrame
    df_metales = pd.DataFrame()
    
    if df.shape[0] < 15:
        return None, None
        
    # Replace whitespace and empty strings with NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
    # Add date
    df['date'] = df_date
    
    # Remove rows with null values
    df = df.dropna(subset=['monetary_unit']) 
    
    # Remove rows where both exchange rates are NaN
    df = df.dropna(subset=['country','exchange_rate_bs', 'exchange_rate_me'], how='all')
    
    # Remove , from specified columns
    df[numeric] = df[numeric].replace({',': ''}, regex=True)

    # Convert specifed columns in 'numeric' list a numerci, forze errors to NaN
    df[numeric] = df[numeric].apply(pd.to_numeric, errors='coerce')

    # Filter to get metals
    raw_metales = df[(df['country'] == 'ORO') | (df['country'] == 'PLATA')]
    df_metales = raw_metales.copy()

    # Remove metals from the original DF
    df = df.drop(raw_metales.index)
    
    # Extract currency
    index_to_keep = df[(df['monetary_unit'] == 'UNIDAD DE FOMENTO DE VIVIENDA') | (df['currency'] == 'Bs/UFV')].index
    if not index_to_keep.empty:
        df = df.loc[:index_to_keep[0]]
    
    return df, df_metales

    
def merge_data(directory_path):
    names_column = ['country', 'monetary_unit', 'currency', 'exchange_rate_bs', 'exchange_rate_me']
    all_df = pd.DataFrame()
    all_df_metals = pd.DataFrame()

    # Process each .ods file in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.ods'):
            file_path = os.path.join(directory_path, file_name)
            df, df_metales = process_file(file_path, names_column)
            
            # If result is None, skip to the next file
            if df is None or df_metales is None:
                continue

            # Concat the results with the global DF
            all_df = pd.concat([all_df, df], ignore_index=True)
            all_df_metals = pd.concat([all_df_metals, df_metales], ignore_index=True)
            
    # Reset index of all_df_metals
    all_df_metals.reset_index(drop=True, inplace=True)

    if 'exchange_rate_bs' in all_df_metals.columns:
        all_df_metals['exchange_rate_me'] = all_df_metals['exchange_rate_bs']
        all_df_metals = all_df_metals.drop(columns=['exchange_rate_bs'])
    else:
        print("La columna 'exchange_rate_bs' no existe en all_df_metals.")
    
    all_df_metals.rename(columns={'country':'metal'}, inplace=True)
    
    # Show the resulting DataFrames
    print(all_df.shape)
    print(all_df_metals.shape)
    
    # Save to a CSV for the tests
    df.to_csv('data/raw_exchange_rates.csv', index=False)
    
    return all_df, all_df_metals

# example of use
# directory_path = 'data' 
# all_df, all_df_metals = merge_data(directory_path)

# load_data_db(all_df, 'raw_exchange_rates')
# load_data_db(all_df_metals, 'raw_metals')