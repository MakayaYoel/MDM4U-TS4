import kagglehub
import os
import shutil
import csv
from datetime import datetime

# Downloads the tesla stock dataset from Kaggle.
def download_dataset() -> None:
    source_path = kagglehub.dataset_download("simronw/tesla-stock-data-2024") + '\\TESLA.csv'
    target_path = 'src/data'

    # Move to project dir
    shutil.move(source_path, target_path)
    print(f"Dataset downloaded successfully at: {target_path}")

def get_data():
    data = []

    # Create clean csv file
    if not os.path.exists('src/data/TESLA_CLEANED.csv'):
        create_clean_data()
    
    with open('src/data/TESLA_CLEANED.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if i == 0 or len(row) == 0:
                continue

            row[1] = float(row[1])
            row[2] = float(row[2])
            
            data.append(row)

    return data


def create_clean_data():
    raw_file_path = 'src/data/TESLA.csv'
    # Check if file exists
    if not os.path.exists(raw_file_path):
        download_dataset()
    
    clean_data = []

    # Extract relevant data (only using close and adj_close because I'm making a simple prediction)
    def extract(row) -> dict:
        return {
            'date': datetime.strptime(row[1], '%m/%d/%y').strftime('%Y-%m-%d'),
            'close': float(row[5]), 
            'adj_close': float(row[6])
        }
    
    # Save data to a new .csv file
    def save(data) -> None:
        with open('src/data/TESLA_CLEANED.CSV', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['date', 'close', "adj_close"])
            writer.writeheader()
            writer.writerows(data)

    # Load CSV
    with open(raw_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            # Skip header row
            if i == 0:
                continue

            clean_data.append(extract(row))
    
    save(clean_data)

    print("Clean .csv file created at: src/data/TESLA_CLEANED.CSV")
        

    
if __name__ == '__main__':
    print(get_data())