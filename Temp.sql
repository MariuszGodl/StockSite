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
