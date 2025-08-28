

def get_company_brutal():
    companies = [ ]
    
    # HUUUGE-S144
    return companies



from dotenv import load_dotenv
import mysql.connector
import csv
import os

load_dotenv()
conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                )
cursor = conn.cursor()
cursor.execute("SELECT * FROM Company")

with open("company_export.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([i[0] for i in cursor.description])  # column headers
    for row in cursor:
        writer.writerow(row)

cursor.close()
conn.close()
