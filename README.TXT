Data Wrangling with European Air Quality Data

This project processes, stores, analyses, and models European Air Quality Data for various pollutants using PostgreSQL and XGBoost. 

There are 2 Methods of running the code.
Method 1 (Segmented): Every pollutant is processed in a separate file. Ideal if you want to run and compare multiple pollutant models side-by-side. ('Source' folder)
Method 2 (Consolidated): Uses a unified workspace where you can easily swap target pollutants within a single Jupyter Notebook.('Source_Method2' folder)

- Source_Task7_Demo is to show that the project automatically works with all other countries that are part of the EEA ecosystem, the demo is done with Albania,
  This can be done directly in your .env folder in root directory by changing the variable: COUNTRY_CODE = 'AL', no need to create a new folder, I just done this for demonstration purposes.

In both cases the Data Analysis, XGBoost models, and Results will be automatically saved to a 'SavedResults' folder.

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


Method 1 (Segmented): all pollutants in seperate file.
1. Open The 'DataPreperation' Folder and select file of pollutant required and run.
2. Open the 'MachineLearningModels'Folder and run for the pollutant selected in previous step.
3. Repeat Instruction 1. & 2. for each pollutant you want to analyse. (Can run everything in each folder one at a time if you want to analyse & model all pollutants)
All results will be automatically saved into a 'SavedResults' folder located in the source folder

Method 2 (Consolidated). If you want a cleaner workspace.
1. Open 'Hourly_DataAanlysis.ipynb' for pollutants ('SO2', 'O3', 'NO2', 'NOXasNO2', 'CO'),
   Open 'Daily_DataAnalysis.ipynb' for pollutants('PM10', 'PM2.5')
2. In the 3rd code cell, update the variable: POLLUTANT = 'your_desired_pollutant'.
3. In the 9th code cell, update the integer in the SQL query to match your pollutant's ID (see reference table below):
   query = f"""SELECT * FROM {table_name} WHERE "Pollutant" = 9;"""
4. Run the notebook.
5. Open the corresponding XGBoost notebook ('Hourly_XGBoost.ipynb' or 'Daily_XGBoost.ipynb')
6. In the 3rd code cell, update the variable: POLLUTANT = 'your_desired_pollutant' and run the notebook 
All results will be automatically saved into a 'SavedResults' folder located in the source folder


Data Output & File Location
As the pipelines run, the following data files and directories are automatically generated:
- Raw Downloaded Data: Saved as '{COUNTRY_CODE}_Air_quality_Data.zip' ( from 'DataIngestion.py')
- Extracted Database Data: The data extracted to go into the database is saved as '{COUNTRY_CODE}_Extracted_Air_quality_Data.zip' (from 'DataToDatabase.py')
- Cleaned Data: Output from the Data Preparation/Analysis phase is saved in the 'Cleaned_Pollutant_Data' folder as '{COUNTRY_CODE}_{POLLUTANT}_Daily_Cleaned.parquet' 
- Model Results: All Data Analysis outputs and XGBoost models and results are automatically saved into a 'SavedResults' folder located in the source folder.

Reference table of Integer IDs for the:
1 = SO2 (Hourly)
5 = PM10 (Daily)
7 = O3 (Hourly)
8 = NO2 (Hourly)
9 = NOXasNO2 (Hourly)
10 = CO (Hourly)
6001 = PM2.5 (Daily)