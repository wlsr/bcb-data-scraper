import psycopg2
import os
from sqlalchemy import create_engine, Numeric, text
from dotenv import load_dotenv

# Load the variables from the .env in the environment
load_dotenv()

# get values from envirenment variables
password = os.getenv('DB_PASSWORD')
user = os.getenv('DB_USER')
name_bd = os.getenv('DB_NAME')
host = os.getenv('HOST')
port = os.getenv('PORT')

# Conection to PostgreSQL financial_data
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{name_bd}')
    
def create_database_if_not_exists(dbname, user, password, host = host, port = port):
    # Conect to the database
    connection = psycopg2.connect(
        dbname=user,
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True  # Required to create the database
    cursor = connection.cursor()
    
    # Check if the database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
    exists = cursor.fetchone()
    
    if not exists:
        # If it not exist, create it
        cursor.execute(f'CREATE DATABASE {dbname}')
        print(f"Database '{dbname}' created successfully.")
    else:
        print(f"Database '{dbname}' already exists")
    
    # Close connection
    cursor.close()
    connection.close()

def drop_table_cascade(engine, table_name):
    """ Drop table with CASCADE option """
    with engine.connect() as connection:
        transaction = connection.begin() 
        connection.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))
        transaction.commit()  # Confirm changes
        print(f"Table {table_name} deleted successfully")
    
def detect_numeric_columns(df):
    """
    Detect columns that are numeric (including integers and floats)
    and returns a dict where float columns are mapped to numeric 
    """
    dtype = {}
    for col in df.select_dtypes(include=['float']).columns:
        dtype[col] = Numeric(precision=18, scale=6)  # Adjust precision and scale as necessary
    return dtype

def load_data_db(df, table):
    
    # Delete current table with dependencies
    drop_table_cascade(engine, table)
    
    # Identify float columns
    dtype_df = detect_numeric_columns(df)
    
    # Load the Dataframes to the corresponding tables
    df.to_sql(table, engine, if_exists='replace', index=False, dtype=dtype_df)
    
# Example of use
create_database_if_not_exists(dbname=name_bd, user=user, password=password)