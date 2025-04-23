import sqlite3
import matplotlib.pyplot as plt


def analyse_data():
    con = sqlite3.connect("Final Project.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM lifespan")
    rows = cur.fetchall() 
    con.close()

    # Based on the life expectancy growth trend in the past two years,
    # the estimated life expectancy in China and Japan in 2024 is calculated
    for row in rows:
        if row[1] == 'CHN' and row[2] == 2022:
            china_2022_lifespan = row[3]
        elif row[1] == 'CHN' and row[2] == 2023:
            china_2023_lifespan = row[3]
        elif row[1] == 'JP' and row[2] == 2022:
            japan_2022_lifespan = row[3]
        elif row[1] == 'JP' and row[2] == 2023:
            japan_2023_lifespan = row[3]
    print(f"The estimated life expectancy in Japan in 2024 will be: {(((china_2023_lifespan - china_2022_lifespan) / china_2022_lifespan) + 1) * china_2023_lifespan:.2f}years old")
    print(f"The estimated life expectancy in Japan in 2024 will be: {(((japan_2023_lifespan - japan_2022_lifespan) / japan_2022_lifespan) + 1) * japan_2023_lifespan:.2f}years old")
    with open("03.result.txt", "w", encoding="utf-8") as f:
        f.write(f"The estimated life expectancy in Japan in 2024 will be: {(((china_2023_lifespan - china_2022_lifespan) / china_2022_lifespan) + 1) * china_2023_lifespan:.2f}years old\n")
        f.write(f"The estimated life expectancy in Japan in 2024 will be: {(((japan_2023_lifespan - japan_2022_lifespan) / japan_2022_lifespan) + 1) * japan_2023_lifespan:.2f}years old")

    # Line chart
    plt.figure(figsize=(12, 6))  
    x = list(range(1975, 2025))
    rows.sort(key=lambda x: x[2])
    china_lifespan_y = [x[3] for x in rows if x[1] == 'CHN']
    japan_lifespan_y = [x[3] for x in rows if x[1] == 'JP']
    plt.plot(x, china_lifespan_y, label='China', color='#D62728', linewidth=2)
    plt.plot(x, japan_lifespan_y, label='Japan', color='#2C2CA0', linewidth=2)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Lifespan (Years)', fontsize=14)
    plt.title('Life Expectancy in China and Japan (1975-2023)', fontsize=16, weight='bold')
    plt.xticks(fontsize=12, rotation=15) 
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5) 
    plt.legend(fontsize=12, loc='best', frameon=True, shadow=True) 
    plt.legend()
    plt.show()


if __name__ == '__main__':
    analyse_data()
