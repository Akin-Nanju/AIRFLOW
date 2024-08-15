#importing all necessary libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import matplotlib.pyplot as plt



#defining a function to extract data from a given url 
def extract():
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
    response = requests.get(url)   #Send HTTP GET request to the given url 
    soup = BeautifulSoup(response.content,'html.parser')
    table = soup.find('table')
    data = []
    for row in table.find_all('tr')[1:]:
        column = row.find_all('td')
        name = column[1].text.strip()
        market_cap = column[2].text.strip()
        data.append({'NAME': name, 'MC_USD_BILLION': market_cap})
    df = pd.DataFrame(data)
    return df
extract()


#defining function for transforming the extracted data
def transform(df):
    df['MC_USD_BILLION'] = pd.to_numeric(df['MC_USD_BILLION'], errors='coerce')
    df['GBP'] = round(df['MC_USD_BILLION']*0.8,2)
    df['EUR'] = round(df['MC_USD_BILLION']*0.93,2)
    df['RS'] = round(df['MC_USD_BILLION']*134.29,2)
    return df


#defining function for log processing
def log_progress(log_points):
    with open('code_log.txt', 'a') as log_file:
        for log_point in log_points:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {log_point}\n")
log_points = [
    "Starting data extraction",
    "Data extraction completed",
    "Starting data transformation",
    "Data transformation completed",
    "Exporting data to CSV",
    "Code execution finished"
]


#defining function for plotting
def plot_banks(df):
    plt.barh(df['NAME'], df['MC_USD_BILLION'], color='aqua')
    plt.xlabel('Market Capitalization (USD Billion)')
    plt.ylabel('Bank')
    plt.title('Largest Banks by Market Capitalization')
    plt.gca().invert_yaxis()  # Invert y-axis to have the largest bank on top
    plt.tight_layout()
    plt.show()


extract_data = extract()
print(transform(extract_data))
a = transform(extract_data)
plot_banks(a)
a.to_csv('largest_banks.csv', index=False)
log_progress(log_points)
print("COMPLETED")