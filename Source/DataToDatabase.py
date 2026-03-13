import os
import zipfile
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

COUNTRY_CODE = os.getenv("COUNTRY_CODE")  

# Folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE_PATH = os.path.join(BASE_DIR, f"{COUNTRY_CODE}_Air_Quality_Data.zip")
EXTRACT_FOLDER = os.path.join(BASE_DIR, f"{COUNTRY_CODE}_Extracted_Air_Quality_Data")
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Unzip Folder
with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_FOLDER)

# Loop to find all Parquet files and load to DB
parquet_files = []
for root, dirs, files in os.walk(EXTRACT_FOLDER): # Goes through sub folders, E1a
    for file in files:
        if file.endswith('.parquet'):
            parquet_files.append(os.path.join(root, file)) # Saves path of parquet file


table_name = f"air_quality_{COUNTRY_CODE.lower()}"

for file_path in parquet_files: # loops through all .parquet files
    df = pd.read_parquet(file_path, engine='pyarrow') 

    # error conditions
    is_sensor_error = (df['Value'] == -999.0) # -999 broken/offline
    is_invalid = (df['Validity'] == -1) # invalid reading/dat
    is_out_of_range = (df['Value'] < 0) & (~is_sensor_error)  # error with sensor (potential callibration error etc)

    df['Quality_Flag'] = 'Good'
    df.loc[is_sensor_error, 'Quality_Flag'] = 'Sensor Error (-999)'
    df.loc[is_invalid, 'Quality_Flag'] = 'Validity Error (-1)'
    df.loc[is_out_of_range, 'Quality_Flag'] = 'Out of Range (<0)'

    # setting all bad flagged values to NaN
    df.loc[df['Quality_Flag'] != 'Good', 'Value'] = np.nan

    df = df.drop(columns=['FkObservationLog'], errors='ignore')

    # Pushing cleaned df to PostgreSQL, 'append' adds to table if exists or creates it if it doesnt exits
    df.to_sql(table_name, engine, if_exists='append', index=False) # index=false so i dont write index to DB
