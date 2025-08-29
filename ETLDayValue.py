from Other.imports import *
from Other.constants import *

load_dotenv()

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="StockInsertion",
        password="StockDataInsertion",
        database="Stock"
    )
    if conn.is_connected():
        print("Connected")

    cursor = conn.cursor()

    # --- Cache Company IDs ---
    cursor.execute("SELECT Identifier, ID FROM Company")
    company_map = dict(cursor.fetchall()) 

    # --- Cache StockExchange ID ---
    cursor.execute("SELECT ID FROM StockExchange WHERE ExchangeName = %s", ("GPW",))
    exchange_ID = cursor.fetchone()
    if exchange_ID:
        exchange_ID = exchange_ID[0]
    else:
        raise ValueError("No StockExchange entry found for GPW")

    # --- Load config ---
    with open(GPW_JSON, 'r') as file:
        config = json.load(file)

    company_info_dict = {}  # {company_ID: [min_date, max_date]}
    list_of_files = [
        f for f in os.listdir(config['downloads_path']) if f.endswith(('.xls', '.xlsx'))
    ]

    # Sort by filename descending (newest first)
    list_of_files.sort(reverse=True)
    print(len(list_of_files))
    for file_name in list_of_files:

        if not file_name.endswith(('.xls', '.xlsx')):
            continue  # skip non-excel files

        file_path = os.path.join(config['downloads_path'], file_name)
        day_prices = pd.read_excel(file_path)

        rows_to_insert = []

        for index, row in day_prices.iterrows():
            company_ID = company_map.get(row["Nazwa"])
            if not company_ID:
                #print(f"No company found with Identifier = {row['Nazwa']}")
                continue

            date_val = pd.to_datetime(row['Data']).strftime('%Y-%m-%d')

            # Add row for bulk insert
            rows_to_insert.append((
                company_ID,
                date_val,
                round(float(row['Kurs otwarcia']), 2),
                round(float(row['Kurs zamknięcia']), 2),
                round(float(row['Kurs min']), 2),
                round(float(row['Kurs max']), 2),
                int(row['Wolumen']),
                int(row['Liczba Transakcji']),
                int(row['Obrót']) * 1000
            ))

            # Track company entry/exit dates
            if company_ID in company_info_dict:
                company_info_dict[company_ID][0] = min(company_info_dict[company_ID][0], date_val)
                company_info_dict[company_ID][1] = max(company_info_dict[company_ID][1], date_val)
            else:
                company_info_dict[company_ID] = [date_val, date_val]

        # --- Bulk insert for one file ---
        if rows_to_insert:
            insert_query = """
                INSERT INTO DayValue (CompanyID, `Date`, `OPEN`, `CLOSE`, `MIN`, `MAX`, Volume, Trades, Turnover)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    `OPEN` = VALUES(`OPEN`),
                    `CLOSE` = VALUES(`CLOSE`),
                    `MIN` = VALUES(`MIN`),
                    `MAX` = VALUES(`MAX`),
                    Volume = VALUES(Volume),
                    Trades = VALUES(Trades),
                    Turnover = VALUES(Turnover)
            """
            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()
            print(f"Inserted {len(rows_to_insert)} rows from {file_name}")

    # --- Bulk insert StockExchangeEntering ---
    enter_rows = []
    for company_ID, (min_date, max_date) in company_info_dict.items():
        enter_rows.append((exchange_ID, company_ID, min_date, None))

    if enter_rows:
        insert_query = """
            INSERT INTO StockExchangeEntering (StockExchangeID, `CompanyID`, `DateOfEntry`, `DateOfExit`)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                `DateOfEntry` = VALUES(`DateOfEntry`),
                `DateOfExit` = VALUES(`DateOfExit`)
        """
        cursor.executemany(insert_query, enter_rows)
        conn.commit()
        print(f"Inserted/Updated {len(enter_rows)} StockExchangeEntering rows")

except mysql.connector.Error as err:
    print(f"MySQL error: {err}")
except FileNotFoundError as fnf_err:
    print(f"File error: {fnf_err}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    try:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()
        print("MySQL connection closed.")
    except NameError:
        pass
