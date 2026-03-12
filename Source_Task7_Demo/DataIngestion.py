# This script interacts with EEA API to download EEA Air Quality Data.

# Using the async endpoint, which is more suitable for larger requests. In this case, two requests are made.
# The first request starts the process, and returns a URL. 
# This URL is the address where the output will become available once the processis complete. 
# The script ends by polling the output URL until the download becomes available.

from datetime import datetime
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Containing email & COUNTRY_CODE
# When changing country change COUNTRY_CODE in .env


COUNTRY_CODE = os.getenv("COUNTRY_CODE")  

apiUrl = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/"
endpoint = "ParquetFile/async"
fileName = f"{COUNTRY_CODE}_Air_Quality_Data.zip"
downloadPath = os.path.dirname(os.path.abspath(__file__)) # current folder
filePath = os.path.join(downloadPath, fileName)
request_body = {
    "countries": [COUNTRY_CODE], # change country code to automate interaction with any other country in the EEA datasetc
    "cities": [],
    "pollutants": ["SO2", "PM10", "O3", "NO2", "NOX as NO2", "CO", "PM2.5"], # capture everything except VOCs (Volatile Organic Compounds)
    "dataset": 2, # dataset 2 is E1a (Primary Validated Data)
    "dateTimeStart": "2013-01-01T00:00:00Z",
    "dateTimeEnd": "2024-12-31T23:59:59Z",
    # "aggregationType": "day",
    "email": os.getenv("EEA_EMAIL")
}

response = requests.post(f"{apiUrl}{endpoint}", json=request_body)
downloadFile = response.text
print(downloadFile)

t_start = datetime.now()
while True:
    if (datetime.now()-t_start).total_seconds() > 3600: # stop after 1 hour if the file has not been created
        break

    parquetResponse = requests.get(downloadFile)

    if parquetResponse.status_code==404: # Not loaded yet
        time.sleep(20) # 20sec pause inisde download loop
    else:
        break

with open(filePath, "wb") as fp:
    fp.write(parquetResponse.content)
