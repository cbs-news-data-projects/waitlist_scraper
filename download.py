from datetime import datetime
import requests
import glob

url = "https://data.sfgov.org/api/views/w4sk-nq57/rows.csv?accessType=DOWNLOAD"


# check if the file for today has already been downloaded
def check_date(today):

    existing_files = glob.glob("waitlist_data/*.csv")
    
    if today in existing_files:
        return False
    else:
        return True

# download the data
def download_data():
    response = requests.get(url)
    with open(f"data/{datetime.now().strftime('%Y-%m-%d')}.csv", "wb") as file:
        file.write(response.content)
    
    return True


if __name__ == "__main__":

    today = datetime.now().strftime("%Y-%m-%d")

    if check_date(today):
        download_data()
        print(f"Downloaded file for {today}")
    else:
        print(f"Already downloaded file for {today}")