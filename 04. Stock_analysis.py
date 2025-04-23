import sqlite3
import matplotlib.pyplot as plt


def analyse_data():
    # Connect to the database
    con = sqlite3.connect("Final Project.db")
    cur = con.cursor() 
    cur.execute("SELECT * FROM stock")
    rows = cur.fetchall()
    # print(rows)
    con.close()

    # Calculate the closing price change in the last 100 days
    close_change = rows[99][3] - rows[0][3]
    print(f"In the last 100 trading days, The closing price change value of {rows[0][1]} is {close_change:.2f} US dollar")
    # Save the calculation results into a text file
    with open("04. result.txt", "w", encoding="utf-8") as f:
        f.write(f"In the last 100 trading days, The closing price change value of {rows[0][1]} is {close_change:.2f} US dollar")

    # Line chart
    x = [row[2] for row in rows]
    y = [row[3] for row in rows]
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, label='Close Price', color='green', linewidth=2)
    plt.title(f"{rows[0][1]} Stock Close Price (Past 100 Days)", fontsize=16, weight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Close Price (USD)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.legend()
    n = 5  # Display every 5 label
    plt.xticks(ticks=range(0, len(x), n), labels=[x[i] for i in range(0, len(x), n)], rotation=15)
    plt.show()


if __name__ == '__main__':
    analyse_data()
