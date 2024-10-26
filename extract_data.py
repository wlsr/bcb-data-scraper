import requests
from datetime import datetime, timedelta
import os
import time

def check_file_exists(file_path):
    # Check if the file exists in the specified path
    return os.path.exists(file_path)

def download_ods_files(start_date, end_date, download_path, delay):
    current_date = start_date

    while current_date <= end_date:
        # skip Saturdays(5) and Sundays(6) 
        if current_date.weekday() not in [5, 6]:  
            url = f"https://www.bcb.gob.bo/librerias/indicadores/otras/otras_imprimir2ODS.php?qdd={current_date.day}&qmm={current_date.month}&qaa={current_date.year}"
            file_name = f"{download_path}/{current_date.strftime('%d-%m-%Y')}.ods"
            
            # Check if the file already exists
            if check_file_exists(file_name):
                print(f"The file {file_name} already exists. jumping to the next day")
                current_date += timedelta(days=1)
                continue  
            
            try:
                # Make a get request to download the file 
                response = requests.get(url)
                response.raise_for_status()  #Throw an error for response codes 4xx and 5xx
                
                # Save the file
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print(f"Archivo descargado: {file_name}")
                
                # Wait a specific time before the next download
                time.sleep(delay)
            except Exception as e:
                print(f"Download ERROR {url}: {e}")

        else:
            print(f"Skipping {current_date.strftime('%Y-%m-%d')} - weekend.")

        current_date += timedelta(days=1)  # Go to the next day

# Example of use
start_date = datetime(2008, 1, 1)
end_date = datetime(2024, 10, 26)
download_path = 'data' 

download_ods_files(start_date, end_date, download_path,delay=0.5)
