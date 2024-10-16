
# BCB Data Scraper

## Description
This project downloads ODS files containing financial data from the Central Bank of Bolivia's website, processes them, and extracts relevant information. It is designed to automate data extraction, cleaning, and merging for further analysis.

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

Make sure to install the necessary packages using:
```bash
pip install requests pandas numpy
```
Script for downloading ODS files
## Project Structure
```
project-directory/
│
├── data/                      # Folder where the ODS files will be saved
├── extract_data.py            # Script for downloading ODS files
├── merge_data.py              # Script for processing and merging data
└── README.md                  # Project documentation
```

## Usage

### Extracting ODS Files
To download the ODS files, run the `extract_data.py` with specified start and end dates:
```python
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 2, 29)
download_path = 'data'  # Ensure this folder exists

download_ods_files(start_date, end_date, download_path, delay=2)
```

### Merging Data
After downloading the files, you can merge and process them using:
```python
all_df, all_df_metales = merge_data('data')
```

## Code Explanation

### Extract Data (`extract_data.py`)
The script downloads ODS files from the Central Bank of Bolivia's website based on a date range. It skips weekends and checks if the file has already been downloaded.

### Merge Script (`merge_data.py`)
This script processes the downloaded files by cleaning the data, filtering out empty rows, separating data related to metals, and merging the files for analysis.

## Considerations
- Ensure that the `data` directory exists before running the scripts.
- Set an appropriate delay between downloads to avoid overloading the server.

## License
This project is licensed under the MIT License.
