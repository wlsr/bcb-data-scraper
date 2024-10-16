import requests
from datetime import datetime, timedelta
import os
import time

def check_file_exists(file_path):
    # Comprobar si el archivo existe en la ruta especificada
    return os.path.exists(file_path)

def download_ods_files(start_date, end_date, download_path, delay):
    current_date = start_date

    while current_date <= end_date:
        # Discriminar sábados (5) y domingos (6)
        if current_date.weekday() not in [5, 6]:  # Si no es sábado ni domingo
            # Construye la URL
            url = f"https://www.bcb.gob.bo/librerias/indicadores/otras/otras_imprimir2ODS.php?qdd={current_date.day}&qmm={current_date.month}&qaa={current_date.year}"
            file_name = f"{download_path}/{current_date.strftime('%d-%m-%Y')}.ods"
            
            # Verificar si el archivo ya existe
            if check_file_exists(file_name):
                print(f"El archivo {file_name} ya existe. Saltando al siguiente día.")
                current_date += timedelta(days=1)
                continue  # Pasar al siguiente día
            
            try:
                # Hacer una solicitud GET para descargar el archivo
                response = requests.get(url)
                response.raise_for_status()  # Lanza un error para códigos de respuesta 4xx y 5xx
                
                
                # Guardar el archivo
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print(f"Archivo descargado: {file_name}")
                
                # Esperar un tiempo específico antes de la siguiente descarga
                time.sleep(delay)
            except Exception as e:
                print(f"Error al descargar {url}: {e}")

        else:
            print(f"Skipping {current_date.strftime('%Y-%m-%d')} - weekend.")

        current_date += timedelta(days=1)  # Avanza al siguiente día

# Ejemplo de uso
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 2, 29)
download_path = 'data'  # Asegúrate de que esta carpeta exista

download_ods_files(start_date, end_date, download_path,delay=2)
