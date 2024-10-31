
# BCB Data Scraper

## Description
This project downloads ODS files containing financial data from the Central Bank of Bolivia's website, processes them, and extracts relevant information. It is designed to automate data extraction, cleaning, and merging for further analysis. This process is part of the ELT pipeline, where data extraction and loading are performed.

## Features
- Download daily financial data in ODS format, skipping weekends.
- Check if a file has already been downloaded to avoid redundancy.
- Process the downloaded ODS files to clean and structure the data.
- Separate and handle data related to metals such as gold and silver.
- Merge data across multiple files for comprehensive analysis.

## Requirements
- Python 3.x
- The following Python packages:
  - `requests`
  - `pandas`
  - `numpy`
  - `datetime`
  - `psycopg2`
  - `others`

Make sure to install the necessary packages using:
```bash
pip install -r requirements.txt
```
Script for downloading ODS files
## Project Structure
```
project-directory/
│
├── data/                      # Folder for saving ODS files
├── connection.py              # Script to manage the connection to the database
├── extract_data.py            # Script to download ODS files
├── merge_data.py              # Script to process and merge data
├── load_data.py               # Script to load data into the database
├── main.py                    # Main script to execute the full ETL pipeline
├── README.md                  # Project documentation
└── requirements.txt           # List of required packages

```

## Usage

### MAIN

``` Python
# Extract

start_date = datetime(2008, 1, 1)
end_date = datetime(2024, 10, 26)
download_path = 'data' 

download_ods_files(start_date, end_date, download_path,delay=0.5)

# Merge

directory_path = 'data' 
all_df, all_df_metals = merge_data(directory_path)

# Load
load_data_db(all_df, 'raw_exchange_rates')
load_data_db(all_df_metals, 'raw_metals')
```

## Code Explanation

### Extract Data (`extract_data.py`)
The script downloads ODS files from the Central Bank of Bolivia's website based on a date range. It skips weekends and checks if the file has already been downloaded.

### Merge Script (`merge_data.py`)
This script processes the downloaded files by cleaning the data, filtering out empty rows, separating data related to metals, and merging the files for analysis.

### Load data (`load_data.py `)
This script load data into the database such as raw_exchange_rates and raw_metals (tables)

## Considerations
- Ensure that the `data` directory exists before running the scripts.
- Set an appropriate delay between downloads to avoid overloading the server.

## License
This project is licensed under the MIT License.
