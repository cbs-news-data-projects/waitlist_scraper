from datetime import datetime
import csv
import requests
import glob

url = "https://data.sfgov.org/api/views/w4sk-nq57/rows.csv?accessType=DOWNLOAD"


# check if the file for today has already been downloaded
def check_date(today):

    existing_files = glob.glob("waitlist_data/*.csv")
    response = requests.get(url)
    new_csv_data = response.content.decode('utf-8').splitlines()
    new_csv_reader = csv.DictReader(new_csv_data)
    new_data_loaded_at = next(new_csv_reader)['data_loaded_at']
    new_loaded_date = datetime.strptime(new_data_loaded_at, "%Y/%m/%d %I:%M:%S %p")

    if not existing_files:
        return True, response.content

    latest_file = max(existing_files, key=lambda x: datetime.strptime(x.split('/')[-1].split('.')[0], "%Y-%m-%d"))

    with open(latest_file, 'r') as file:
        reader = csv.DictReader(file)
        data_loaded_at = next(reader)['data_loaded_at']
        last_loaded_date = datetime.strptime(data_loaded_at, "%Y/%m/%d %I:%M:%S %p")

    return new_loaded_date > last_loaded_date, response.content

# download the data
def download_data():
    response = requests.get(url)
    with open(f"waitlist_data/{datetime.now().strftime('%Y-%m-%d')}.csv", "wb") as file:
        file.write(response.content)
    
    return True


if __name__ == "__main__":

    today = datetime.now().strftime("%Y-%m-%d")

    should_download, new_csv_content = check_date(today)
    if should_download:
        with open(f"waitlist_data/{today}.csv", "wb") as file:
            file.write(new_csv_content)
        print(f"Downloaded file for {today}")
    else:
        print(f"Already downloaded file for {today}")
