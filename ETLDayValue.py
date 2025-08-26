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

    with open(GPW_JSON, 'r') as file:
        config = json.load(file)

    company_info = [] # [[names, date_entry, date_exit]]
    k = 0
    for file_name in os.listdir(config['downloads_path']):
        k += 1
        if k == 10:
            break
        if not file_name.endswith(('.xls', '.xlsx')):
            continue  # skip non-excel files
        
        file_path = os.path.join(config['downloads_path'], file_name)
        day_prices = pd.read_excel(file_path)
        
        for index, row in day_prices.iterrows():
        # -- DayValue Table
        # CREATE TABLE DayValue (
        #     ID INT AUTO_INCREMENT PRIMARY KEY,
        #     CompanyID INT NOT NULL,
        #     `Date` DATE NOT NULL,
        #     `OPEN` DECIMAL(10,2) NOT NULL,
        #     `CLOSE` DECIMAL(10,2) NOT NULL,
        #     `MIN` DECIMAL(10,2) NOT NULL,
        #     `MAX` DECIMAL(10,2) NOT NULL,
        #     Volume INT NOT NULL,
        #     Trades INT NOT NULL,
        #     Turnover DECIMAL(10,2) NOT NULL,

        #     FOREIGN KEY (CompanyID) REFERENCES Company(ID) ON DELETE CASCADE,
        #     UNIQUE (CompanyID, `Date`)
        # );

            select_query = "SELECT ID FROM Company WHERE Identifier = %s"

            cursor.execute(select_query, (row["Nazwa"],))
            company_ID = cursor.fetchone() 
            
            if company_ID:

                company_ID = company_ID[0]
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
                date_val = pd.to_datetime(row['Data']).strftime('%Y-%m-%d')
                cursor.execute(insert_query, (
                    company_ID,
                    date_val,  # Ensure this is in proper date format
                    float(row['Kurs otwarcia']),
                    float(row['Kurs zamknięcia']),
                    float(row['Kurs min']),
                    float(row['Kurs max']),
                    int(row['Wolumen']),
                    int(row['Liczba Transakcji']),
                    float(row['Obrót']) * 1000
                ))
                conn.commit()

                found = False
                for i in range(len(company_info)):
                    if company_ID == company_info[i][0]:
                        found = True
                        if date_val < company_info[i][1]:
                            company_info[i][1] = date_val
                        elif date_val > company_info[i][2]:
                            company_info[i][2] = date_val
                        break
                    
                if not found:               
                    company_info.append([company_ID, date_val, date_val])


            else:
                print(f"No company found with Identifier = {row['Nazwa']}")

# -- StockExchangeEntering Table
# CREATE TABLE StockExchangeEntering (
#     StockExchangeID INT NOT NULL,
#     CompanyID INT NOT NULL,
#     DateOfEntry DATE NOT NULL,
#     DateOfExit DATE,

#     PRIMARY KEY (StockExchangeID, CompanyID),
#     INDEX idx_CompanyID (CompanyID),
#     INDEX idx_StockExchangeID (StockExchangeID),

#     FOREIGN KEY (StockExchangeID) REFERENCES StockExchange(ID),
#     FOREIGN KEY (CompanyID) REFERENCES Company(ID)
# );

# CREATE TABLE Company (
#     ID INT AUTO_INCREMENT PRIMARY KEY,
#     Identifier VARCHAR(10) NOT NULL CHECK (Identifier REGEXP '^[A-Za-z0-9 ]+$'), 
#     CompanyName VARCHAR(100) NOT NULL CHECK (CompanyName REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     CEO VARCHAR(100) NOT NULL CHECK (CEO REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     Industry VARCHAR(100) NOT NULL CHECK (Industry REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     Info VARCHAR(5000) NOT NULL,
#     NrOfShares INT NOT NULL CHECK (NrOfShares > 0),
#     Country VARCHAR(100) NOT NULL CHECK (Country REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     City VARCHAR(100) NOT NULL CHECK (City REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     CreationDate DATE NOT NULL,
#     DestructionDate DATE,
#     UNIQUE(Identifier)
# );
# -- StockExchange Table
# CREATE TABLE StockExchange (
#     ID INT AUTO_INCREMENT PRIMARY KEY,
#     ExchangeName VARCHAR(100) NOT NULL CHECK (ExchangeName REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     Country VARCHAR(100) NOT NULL CHECK (Country = 'Polska'),
#     City VARCHAR(100) NOT NULL CHECK (City REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
#     UNIQUE(ExchangeName)
# );


    for i in range(len(company_info)):

        company_ID = company_info[i][0]
        select_query = "SELECT ID FROM StockExchange WHERE ExchangeName = %s"
        
        cursor.execute(select_query, ("GPW",))
        exchanenge_ID = cursor.fetchone()
        exchanenge_ID = exchanenge_ID[0]

        insert_query = """
            INSERT INTO StockExchangeEntering (StockExchangeID, `CompanyID`, `DateOfEntry`, `DateOfExit`)
            VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    `StockExchangeID` = VALUES(`StockExchangeID`),
                    `CompanyID` = VALUES(`CompanyID`),
                    `DateOfEntry` = VALUES(`DateOfEntry`),
                    `DateOfExit` = VALUES(`DateOfExit`)
                """

        cursor.execute(insert_query, (
            exchanenge_ID,
            company_ID,
            company_info[i][1],
            None))
        conn.commit()
        print("Data added")

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
