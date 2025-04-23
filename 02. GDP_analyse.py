import sqlite3
import matplotlib.pyplot as plt


def analyse_data():
    con = sqlite3.connect("Final Project.db")
    cur = con.cursor()  
    cur.execute("SELECT * FROM gdp")
    rows = cur.fetchall() 
    con.close()

    for row in rows:
        if row[1] == 'CHN' and row[2] == 2023:
            china_2023_gdp = row[3]
        elif row[1] == 'CHN' and row[2] == 2024:
            china_2024_gdp = row[3]
        elif row[1] == 'USA' and row[2] == 2023:
            usa_2023_gdp = row[3]
        elif row[1] == 'USA' and row[2] == 2024:
            usa_2024_gdp = row[3]
    print(f"China's GDP growth rate in 2023-2024 is {(china_2024_gdp - china_2023_gdp) / china_2023_gdp * 100:.2f}%")
    print(f"U.S. GDP growth rate for 2023-2024 is {(usa_2024_gdp - usa_2023_gdp) / usa_2023_gdp * 100:.2f}%")

    with open("02.result.txt", "w", encoding="utf-8") as f:
        f.write(f"China's GDP growth rate in 2023-2024 {(china_2024_gdp - china_2023_gdp) / china_2023_gdp * 100:.2f}%\n")
        f.write(f"U.S. GDP growth rate for 2023-2024 {(usa_2024_gdp - usa_2023_gdp) / usa_2023_gdp * 100:.2f}%")

    x = list(range(1980, 2030))
    china_gdp_y = [x[3] for x in rows if x[1] == 'CHN']
    usa_gdp_y = [x[3] for x in rows if x[1] == 'USA']
    plt.plot(x, china_gdp_y, label='China', color='red', linewidth=3)
    plt.plot(x, usa_gdp_y, label='USA', color='green', linewidth=3)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('GDP (Trillions of USD)', fontsize=12)
    plt.title('GDP Analysis')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    analyse_data()
