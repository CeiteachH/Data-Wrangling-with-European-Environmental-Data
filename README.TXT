Data Wrangling with European Air Quality Data

This project processes, stores, analyses, and models European Air Quality Data for various pollutants using PostgreSQL and XGBoost. 

Method:
Every pollutant is processed in a separate file. Ideal for running and compare multiple pollutant models side-by-side. ('Source' folder)

- Source_Task7_Demo is to show that the project automatically works with all other countries that are part of the EEA ecosystem, the demo is done with Albania,
  This can be done directly in your .env folder in root directory by changing the variable: COUNTRY_CODE = 'AL', no need to create a new folder, I just done this for demonstration purposes.

The Data Analysis Plots, XGBoost models, and Results will be automatically saved to a 'SavedResults' folder.

Prerequesites
- Python (I am using 3.13.0)
- PostgreSQL (I am using PostgreSQL 18.2 on x86_64-windows, compiled by msvc-19.44.35222, 64-bit)
- Python packages (I pip installed) ( visible in cell 1 of each notebook and at top of py scripts)

Instructions to run the project:
1. Clone this repository
2. Create .env file in root directory
   EEA_EMAIL=your_email@example.com
   COUNTRY_CODE= 'IE'  # Code of country to analyse (e.g., 'IE' for Ireland, 'AL' for Albania)
   DB_USER=your_postgresql_username
   DB_PASS=your_database_password
   DB_HOST=localhost # Or your specific host
   DB_PORT=5432      # Default Postgres port
   DB_NAME=your_database_name
   BASE_DATA_PATH=/path/to/your/source/Cleaned_Pollutant_Data
   RESULTS_SAVE_FOLDER=/path/to/your/source/SavedResults

3. Run the following scripts in order from terminal
   python DataIngestion.py
   pyton DataToDatabase.py

4. Run the notebooks for each of the pollutants
   - Open The 'DataPreperation' Folder and select file of pollutant required and run.
   - Open the 'MachineLearningModels'Folder and run for the pollutant selected in previous step.
   Repeat Instruction 4 for each pollutant you want to analyse.

Data Output & File Location
As the pipelines run, the following data files and directories are automatically generated:
- Raw Downloaded Data: Saved as '{COUNTRY_CODE}_Air_quality_Data.zip' ( from 'DataIngestion.py')
- Extracted Database Data: The extracted zip saved as '{COUNTRY_CODE}_Extracted_Air_quality_Data', the invalid readings are assigned NaNs and loaded to database (from 'DataToDatabase.py')
- Cleaned Data: Output from the Data Preparation/Analysis phase is saved in the 'Cleaned_Pollutant_Data' folder as '{COUNTRY_CODE}_{POLLUTANT}_Daily_Cleaned.parquet' 
- Model Results: All Data Analysis outputs and XGBoost models and results are automatically saved into a 'SavedResults' folder located in the source folder.

Reference table of Integer IDs for the:
1 = SO2 (Hourly)
5 = PM10 (Daily)
7 = O3 (Hourly) -8hr cycle
8 = NO2 (Hourly)
9 = NOXasNO2 (Hourly)
10 = CO (Hourly) - 8hr cycle
6001 = PM2.5 (Daily)