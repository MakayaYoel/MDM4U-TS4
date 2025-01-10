import kagglehub
import os
import shutil
import csv
from datetime import datetime
import pandas

# Downloads the tesla stock dataset from Kaggle.
def download_dataset() -> None:
    source_path = kagglehub.dataset_download("simronw/tesla-stock-data-2024") + '\\TESLA.csv'
    target_path = 'src/data'

    # Move to project dir
    shutil.move(source_path, target_path)
    print(f"Dataset downloaded successfully at: {target_path}")

# Returns the Tesla stock data from 2021 - 2024
def get_data() -> list[dict]:
    data = []

    # Create clean csv file
    if not os.path.exists('src/data/TESLA_CLEANED.csv'):
        create_clean_data()
    
    with open('src/data/TESLA_CLEANED.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if i == 0 or len(row) == 0:
                continue

            # because for some reason the price are converted right back to strings...
            data.append({'date': pandas.to_datetime(row[0]), 'adj_close': float(row[1])})

    return data


def create_clean_data() -> None:
    raw_file_path = 'src/data/TESLA.csv'
    # Check if file exists
    if not os.path.exists(raw_file_path):
        download_dataset()
    
    clean_data = []

    # Extract relevant data (only using adj_close because I'm making a simple prediction)
    def extract(row) -> dict:
        return {
            'date': datetime.strptime(row[1], '%m/%d/%y').strftime('%Y-%m-%d'),
            'adj_close': float(row[6])
        }
    
    # Save data to a new .csv file
    def save(data) -> None:
        with open('src/data/TESLA_CLEANED.CSV', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['date', 'adj_close'])
            writer.writeheader()
            writer.writerows(data)

    # Load CSV
    with open(raw_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            # Skip header row and only use stock prices from 2021 - 2024
            if i == 0 or not row[1][-2:] in ['21', '22', '23', '24']:
                continue

            clean_data.append(extract(row))
    
    save(clean_data)
    print("Clean .csv file created at: src/data/TESLA_CLEANED.CSV")
        

    
if __name__ == '__main__':
    # Test get_data()
    print(get_data())