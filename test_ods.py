
import pandas as pd
import numpy as np

column_names = ['country', 'monetary_unit', 'currency', 'exchange_rate_bs', 'exchange_rate_me']

df = pd.read_excel('data/31-12-2021.ods', engine='odf', index_col=False,usecols='A:E')
# Reemplazar espacios en blanco y cadenas vacías con NaN
#df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
print(df.head(20))
print(df.columns)