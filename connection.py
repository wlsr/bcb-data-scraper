import psycopg2
from sqlalchemy import create_engine, Numeric

user = "postgres"
password = "sistemas19"
name_bd = 'financial_data'

def create_database_if_not_exists(dbname, user, password, host='localhost', port='5432'):
    # Conectar a la base de datos PostgreSQL (por defecto)
    connection = psycopg2.connect(
        dbname='postgres',
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True  # Necesario para crear la base de datos
    cursor = connection.cursor()
    
    # Verificar si la base de datos ya existe
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
    exists = cursor.fetchone()
    
    if not exists:
        # Si la base de datos no existe, crearla
        cursor.execute(f'CREATE DATABASE {dbname}')
        print(f"Base de datos '{dbname}' creada exitosamente.")
    else:
        print(f"La base de datos '{dbname}' ya existe.")
    
    # Cerrar la conexión
    cursor.close()
    connection.close()
    
def detect_numeric_columns(df):
    """
    Detecta las columnas que son numéricas (incluyendo enteros y flotantes)
    y devuelve un diccionario donde las columnas flotantes se asignan a Numeric.
    """
    dtype = {}
    for col in df.select_dtypes(include=['float']).columns:
        dtype[col] = Numeric(precision=18, scale=6)  # Ajusta precision y scale según sea necesario
    return dtype

def load_data_db(df1, df2):
    # Conexión a PostgreSQLfinancial_data
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost/{name_bd}')
    
    # Detectar las columnas flotantes en cada DataFrame
    dtype_df1 = detect_numeric_columns(df1)
    dtype_df2 = detect_numeric_columns(df2)
    
    # Cargar los DataFrames a las tablas correspondientes
    df1.to_sql('exchange_rates', engine, if_exists='append', index=False, dtype=dtype_df1)
    df2.to_sql('metals', engine, if_exists='append', index=False, dtype=dtype_df2)
    
# Ejemplo de uso
create_database_if_not_exists(dbname=name_bd, user=user, password=password)
