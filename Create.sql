USE Stock;

-- Drop tables safely in the correct order due to foreign key dependencies
DROP TABLE IF EXISTS StockExchangeEntering;
DROP TABLE IF EXISTS DayValue;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS StockExchange;
DROP TRIGGER IF EXISTS check_dates_company_insert;
DROP TRIGGER IF EXISTS check_dates_company_update;
DROP TRIGGER IF EXISTS check_dates_StockExchangeEntering_insert;
DROP TRIGGER IF EXISTS check_dates_StockExchangeEntering_update;

-- StockExchange Table
CREATE TABLE StockExchange (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ExchangeName VARCHAR(100) NOT NULL CHECK (ExchangeName REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
    Country VARCHAR(100) NOT NULL CHECK (Country = 'Polska'),
    City VARCHAR(100) NOT NULL CHECK (City REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$')
);

-- Company Table
CREATE TABLE Company (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Identifier VARCHAR(10) NOT NULL CHECK (Identifier REGEXP '^[A-Za-z0-9 ]+$'), 
    CompanyName VARCHAR(100) NOT NULL CHECK (CompanyName REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
    CEO VARCHAR(100) NOT NULL CHECK (CEO REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
    Industry VARCHAR(100) NOT NULL CHECK (Industry REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
    Info VARCHAR(5000) NOT NULL,
    NrOfShares INT NOT NULL CHECK (NrOfShares > 0),
    Capitalization INT NOT NULL,
    Country VARCHAR(100) NOT NULL CHECK (Country REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
    City VARCHAR(100) NOT NULL CHECK (City REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$'),
    CreationDate DATE NOT NULL,
    DestructionDate DATE 
);



CREATE TRIGGER check_dates_company_insert BEFORE INSERT ON Company
FOR EACH ROW
BEGIN 
    IF NEW.DestructionDate IS NOT NULL AND NEW.DestructionDate < NEW.CreationDate THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DestructionDate must be NULL or after creation';
    END IF;
END ;

CREATE TRIGGER check_dates_company_update BEFORE UPDATE ON Company
FOR EACH ROW
BEGIN 
    IF NEW.DestructionDate IS NOT NULL AND NEW.DestructionDate < NEW.CreationDate THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DestructionDate must be NULL or after creation';
    END IF;
END ;



-- StockExchangeEntering Table
CREATE TABLE StockExchangeEntering (
    StockExchangeID INT NOT NULL,
    CompanyID INT NOT NULL,
    DateOfEntry DATE NOT NULL,
    DateOfExit DATE,

    PRIMARY KEY (StockExchangeID, CompanyID),
    INDEX idx_CompanyID (CompanyID),
    INDEX idx_StockExchangeID (StockExchangeID),

    FOREIGN KEY (StockExchangeID) REFERENCES StockExchange(ID),
    FOREIGN KEY (CompanyID) REFERENCES Company(ID)
);



CREATE TRIGGER check_dates_StockExchangeEntering_insert BEFORE INSERT ON StockExchangeEntering
FOR EACH ROW 
BEGIN
    IF NEW.DateOfExit IS NOT NULL AND NEW.DateOfExit < NEW.DateOfEntry THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DateOfExit must be NULL or after DateOfEntry';
    END IF;
END;

CREATE TRIGGER check_dates_StockExchangeEntering_update BEFORE UPDATE ON StockExchangeEntering
FOR EACH ROW
BEGIN
    IF NEW.DateOfExit IS NOT NULL AND NEW.DateOfExit < NEW.DateOfEntry THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DateOfExit must be NULL or after DateOfEntry';
    END IF;
END;


-- DayValue Table
CREATE TABLE DayValue (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CompanyID INT NOT NULL,
    `Date` DATE NOT NULL,
    `OPEN` DECIMAL(10,2) NOT NULL,
    `CLOSE` DECIMAL(10,2) NOT NULL,
    `MIN` DECIMAL(10,2) NOT NULL,
    `MAX` DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (CompanyID) REFERENCES Company(ID) ON DELETE CASCADE,
    UNIQUE (CompanyID, `Date`)
);

