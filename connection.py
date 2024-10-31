import psycopg2

def create_database_if_not_exists(dbname, user, password, host, port):
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

# Example of use
#create_database_if_not_exists(dbname=name_bd, user=user, password=password)