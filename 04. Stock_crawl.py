import yfinance as yf
import sqlite3


# Get data
def get_stock_data(stock_code, start_date, end_date):
    # Read all stored data
    cur.execute(f"SELECT * FROM stock where stock_code = '{stock_code}'")
    rows = cur.fetchall()
    count = len(rows) // 25  # Every 25 data items are grouped together
    if count == 4:
        print("Data has been stored 4 times, 25 data each time, a total of 100 data. No new data will be collected!")
        exit()
    print(f"Number of times of {stock_code} stock data was collected: {count + 1}")


    data = yf.download(stock_code, start=start_date, end=end_date)
    x = list(data.index.strftime('%Y-%m-%d'))
    y = [i[0] for i in data['Close'].values]

    # Limit each code run to only collect and store 25 pieces of data, and do not store data repeatedly
    datas = []
    for i in range((count*25), (count*25+25)):
        datas.append((stock_code, x[i], float(y[i])))
    cur.executemany("""
        INSERT INTO stock (stock_code, date, close)
        VALUES (?,?,?)
    """, datas)
    con.commit()
    print(datas)


if __name__ == '__main__':
    con = sqlite3.connect('Final Project.db')
    cur = con.cursor()
    # Create a data table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            stock_code VARCHAR(128),
            date VARCHAR(128),
            close REAL
        );
    """)
    # Set the stock code
    stock_code = "NVDA"  # NVIDIA Corporation
    # 100 days
    start = "2024-11-21"
    end = "2025-04-21"
    get_stock_data(stock_code, start, end)
    # Exit
    cur.close()
    con.close()
