CREATE USER 'StockInsertion'@'localhost' IDENTIFIED BY 'StockDataInsertion';
GRANT INSERT, UPDATE ON Stock.* TO 'StockInsertion'@'localhost';
