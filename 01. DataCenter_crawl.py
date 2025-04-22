import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to the database (if it does not exist, a new database file will be created)
con = sqlite3.connect("Final Project.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS data_center_countries (
        id INTEGER PRIMARY KEY,
        country_name VARCHAR(128)
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS data_centers (
        id INTEGER PRIMARY KEY,
        country_id INTEGER,
        center_name VARCHAR(128),
        total_space INTEGER,
        FOREIGN KEY (country_id) REFERENCES data_center_countries(id)
    );
""")


# Get data
def get_data(url, country_id):

    r = requests.get(url).json()
    locations = r['locations']['preloadedSearchLocations']
    # Get detailed information of data_center one by one
    for location in locations:
        detail_url = f"https://www.datacenters.com/{location['url']}"
        # print(detail_url)
        r = requests.get(detail_url).text
        soup = BeautifulSoup(r, 'html.parser')
        name_tag = soup.find(id='locationName')
        name = name_tag.get_text(strip=True) if name_tag else 'N/A'
        total_space = soup.select_one('#totalSpace > div:nth-of-type(2) > strong')
        if total_space:
            total_space = total_space.get_text(strip=True)
            total_space = total_space.replace('sqft', '').strip()
        else:  # Some data has no total space information, skip
            continue
        print(f"Name: {name}  Total Space: {total_space}")
        datas.append((country_id, name, total_space))
        # When the cached data reaches 20, it will be stored in the database at one time
        if len(datas) == 20:  
            cur.executemany("""
                INSERT INTO data_centers (country_id, center_name, total_space)
                VALUES (?,?,?)
            """, datas)
            con.commit()
            exit()


if __name__ == '__main__':
    datas = []

    # United States Data Centers(Most Popular)
    cur.execute(f"SELECT * FROM data_centers where country_id=1") # Read all stored United States data
    rows = cur.fetchall() 
    count = len(rows) // 20 # Calculate the number of stored data groups based on 20 data sets
    if count == 3:
        print(f"United States: Data has been stored 3 times, 20 data each time, a total of 60 data. No new data will be collected!")
    else:
        print(f"United States: Number of data collection times: {count + 1}")
        if count == 0:  # Only store country information when collecting data for the first time
            cur.execute("""
                INSERT INTO data_center_countries (id, country_name)
                VALUES (1, 'United States');
            """)
        # Page number (40 data items per page, but considering that some data items do not have total space information, crawling 1 page should be enough to get 25 data items)   
        for page in range(count+1, count+2):  
            url = (f"https://www.datacenters.com/api/v1/locations/countries/234?query=&page={page}&sort_by=preloaded_search_locations.recent_visits_count&sort_direction=desc&radius=100")
            get_data(url, 1)  # Get data

    # United Kingdom Data Centers(Most Popular)
    cur.execute(f"SELECT * FROM data_centers where country_id=2")  # Read all stored United Kingdom data
    rows = cur.fetchall()  
    count = len(rows) // 20 # Calculate the number of stored data groups based on 20 data sets
    if count == 2:
        print(f"United Kingdom: Data has been stored 2 times, 20 data each time, a total of 40 data. No new data will be collected!")
    else:
        print(f"United Kingdom: Number of data collection times: {count + 1}")
        # Only store country information when collecting data for the first time
        if count == 0: 
            cur.execute("""
                INSERT INTO data_center_countries (id, country_name)
                VALUES (2, 'United Kingdom');
            """)
        for page in range(count+1, count+2):  # Page
            url = (f"https://www.datacenters.com/api/v1/locations/countries/77?query=&page={page}&sort_by=preloaded_search_locations.recent_visits_count&sort_direction=desc&radius=100")
            get_data(url, 2)  # Get data

    # Exit
    cur.close()
    con.close()
