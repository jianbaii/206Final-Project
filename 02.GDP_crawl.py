import requests
import sqlite3


def get_gdp_data(api_url, country_code):

    cur.execute(f"SELECT * FROM gdp where country_code = '{country_code}'")  
    rows = cur.fetchall()  
    count = len(rows)//10  
    if count == 5:
        print("Data has been stored 5 times, 20 data each time, for a total of 100 data. No new data will be collected!")
        exit()
    print(f"{count+1} collection of {country_code} data")


    response = requests.get(api_url)
    r = response.json()
    r = r['values']['NGDPD'][country_code]

   
    datas = []  
    l = list(r.items())
    for i in l[(count*10):(count*10+10)]:
        datas.append((country_code, int(i[0]), i[1]))
    cur.executemany("""
        INSERT INTO gdp (country_code, year, gdp)
        VALUES (?,?,?)
    """, datas)
    con.commit()
    print(datas)


if __name__ == '__main__':
    api_url = "https://www.imf.org/external/datamapper/api/v1/NGDPD"
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gdp (
            id INTEGER PRIMARY KEY,
            country_code VARCHAR(128),
            year INTEGER,
            gdp REAL
        );
    """)
    get_gdp_data(api_url, "CHN")
    get_gdp_data(api_url, "USA")

    cur.close()
    con.close()
