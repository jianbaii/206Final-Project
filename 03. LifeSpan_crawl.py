import requests
import sqlite3



def get_life_data(country_code):
 
    cur.execute(f"SELECT * FROM lifespan where country_code = '{country_code}'")  
    rows = cur.fetchall()
    count = len(rows) // 10 
    if count == 5:
        print("Data has been stored 5 times, 20 data each time, a total of 100 data. No new data will be collected!")
        exit()
    print(f"Numbers of time to get data from {country_code}: {count + 1}")

  
    api_url = f'https://api.worldbank.org/v2/country/{country_code}/indicator/SP.DYN.LE00.IN?format=json'
    response = requests.get(api_url)
    r = response.json()
    r = r[1]

  
    datas = [] 
    for i in r[(count*10):(count*10+10)]:
        datas.append((country_code, i['date'], i['value']))
    cur.executemany("""
        INSERT INTO lifespan (country_code, year, value)
        VALUES (?,?,?)
    """, datas)
    con.commit()
    print(datas)


if __name__ == '__main__':
    con = sqlite3.connect('Final Project.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lifespan (
            id INTEGER PRIMARY KEY,
            country_code VARCHAR(128),
            year INTEGER,
            value REAL
        );
    """)
    get_life_data("CHN")
    get_life_data("JP")
    cur.close()
    con.close()


