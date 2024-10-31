from extract_data import *
from merge_data import *
from load_data import *

def main():
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
    
if __name__ == "__main__":
    main()