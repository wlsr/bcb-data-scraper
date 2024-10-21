import psycopg2
import os
from sqlalchemy import create_engine, Numeric
from dotenv import load_dotenv

# Cargar las variables del archivo .env en el entorno
load_dotenv()

# Obtener la contraseña desde la variable de entorno
password = os.getenv('DB_PASSWORD')
user = os.getenv('DB_USER')
name_bd = os.getenv('DB_NAME')


# Conexión a PostgreSQLfinancial_data
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost/{name_bd}')
    
def create_database_if_not_exists(dbname, user, password, host='localhost', port='5432'):
    # Conectar a la base de datos PostgreSQL (por defecto)
    connection = psycopg2.connect(
        dbname=user,
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

def load_data_db(df, table):
 
    # Detectar las columnas flotantes en cada DataFrame
    dtype_df = detect_numeric_columns(df)
    
    # Cargar los DataFrames a las tablas correspondientes
    df.to_sql(table, engine, if_exists='replace', index=False, dtype=dtype_df)
    
# Ejemplo de uso
create_database_if_not_exists(dbname=name_bd, user=user, password=password)
