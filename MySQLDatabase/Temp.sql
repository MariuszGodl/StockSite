CREATE USER 'StockInsertion'@'localhost' IDENTIFIED BY 'StockDataInsertion';
GRANT SELECT, INSERT, UPDATE ON Stock.* TO 'StockInsertion'@'localhost';

USE Stock;
ALTER TABLE Company
ADD COLUMN IDENTIFIER VARCHAR(10) NOT NULL
CHECK (IDENTIFIER REGEXP '^[A-Za-z0-9 ]+$');


SELECT VERSION();


USE Stock;
SELECT * FROM StockExchange
SELECT * FROM Company
SELECT * FROM DayValue
SELECT * FROm StockExchangeEntering

TRUNCATE TABLE DayValue;
TRUNCATE TABLE StockExchangeEntering;
TRUNCATE TABLE Company;
TRUNCATE TABLE StockExchange;



SELECT 
    table_schema AS `Database`, 
    ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 2) AS `Size_in_GB`
FROM 
    information_schema.tables
WHERE 
    table_schema = 'Stock'
GROUP BY 
    table_schema;
