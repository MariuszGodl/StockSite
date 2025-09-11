import mysql.connector
from mysql.connector import Error

def insert_stock_exchange():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",       # replace with your MySQL user
            password="Kanakan9824",   # replace with your password
            database="Stock"    # replace with your DB name (e.g., Stock)
        )
        if conn.is_connected():
            print("Connected to database")

        cursor = conn.cursor()

        insert_query = """
            INSERT INTO StockExchange (ExchangeName, Country, City)
            VALUES (%s, %s, %s)
        """

        data = ("GPW", "Polska", "Warszawa")

        cursor.execute(insert_query, data)
        conn.commit()
        print("Record inserted successfully")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    insert_stock_exchange()
