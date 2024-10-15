import requests
import time
import os
from datetime import datetime, timedelta

# Definir el rango de fechas
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 31)  # Cambia según el rango deseado

current_date = start_date

while current_date <= end_date:
    # Construye la URL
    url = f"https://www.bcb.gob.bo/librerias/indicadores/otras/otras_imprimir2ODS.php?qdd={current_date.day}&qmm={current_date.month}&qaa={current_date.year}"
    
    # Definir el nombre del archivo
    file_name = f"data/{current_date.day}-{current_date.month}-{current_date.year}.ods"
    
    # Verificar si el archivo ya existe
    if os.path.exists(file_name):
        print(f"El archivo {file_name} ya existe. Saltando al siguiente día.")
        current_date += timedelta(days=1)
        continue  # Pasar al siguiente día
    
    try:
        # Hacer una solicitud GET para descargar el archivo
        response = requests.get(url)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Guardar el archivo
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Archivo guardado: {file_name}")
        else:
            print(f"Error al descargar el archivo para {current_date}: {response.status_code}")
    
    except Exception as e:
        print(f"Ocurrió un error al descargar el archivo para {current_date}: {e}")
    
    # Pausa entre solicitudes para evitar ser bloqueado
    time.sleep(10)  # Pausa de 5 segundos (puedes ajustar el tiempo según sea necesario)

    # Avanza al siguiente día
    current_date += timedelta(days=1)
