import sqlite3
import matplotlib.pyplot as plt


def analyse_data():
    # Connecting to a database
    con = sqlite3.connect("Final Project.db")
    cur = con.cursor()
    # Query United States data
    query = """
        SELECT dc.*
        FROM data_centers dc
        JOIN data_center_countries dcc ON dc.country_id = dcc.id
        WHERE dcc.country_name = ?;
    """
    cur.execute(query, ('United States',))
    rows = cur.fetchall()  # Get all data
    united_states = [x[3] for x in rows]
    # Query the United Kingdom data
    query = """
        SELECT dc.*
        FROM data_centers dc
        JOIN data_center_countries dcc ON dc.country_id = dcc.id
        WHERE dcc.country_name = ?;
    """
    cur.execute(query, ('United Kingdom',))
    rows = cur.fetchall()  # Get all data
    united_kingdom = [x[3] for x in rows]
    # Close the database connection
    con.close()

    # Calculate the average space capacity of the most popular data centers in the United States and the United Kingdom
    united_states_avg = sum(united_states) / len(united_states)
    united_kingdom_avg = sum(united_kingdom) / len(united_kingdom)
    # Output
    print("The average space capacity of the most popular data centers in the United States and the United Kingdom is:")
    print(f"United States: {united_states_avg:.2f} sqft")
    print(f"United Kingdom: {united_kingdom_avg:.2f} sqft")
   # Save the calculation results into a text file
    with open("01.result.txt", "w", encoding="utf-8") as f:
        f.write(f"The average space capacity of the most popular data centers in the United States and the United Kingdom is: \n")
        f.write(f"United States: {united_states_avg:.2f} sqft\n")
        f.write(f"United Kingdom: {united_kingdom_avg:.2f} sqft")

    # Bar chart
    x = ["United States", "United Kingdom"]
    y = [united_states_avg, united_kingdom_avg]
    plt.bar(x, y, color=['blue', 'green'], edgecolor='black', width=0.6)
    plt.xlabel("country")
    plt.ylabel("Space (sqft)")
    plt.title("Data Center Average Space")
    plt.show()

    # Pie chart
    labels = ["United States", "United Kingdom"]
    sizes = [united_states_avg, united_kingdom_avg]
    colors = ['blue', 'green']
    plt.pie(sizes, labels=labels, textprops={'color': "white"}, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.legend()
    plt.title("Data Center Average Space")
    plt.show()


if __name__ == '__main__':
    analyse_data()
