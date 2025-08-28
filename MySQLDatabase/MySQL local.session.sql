DESCRIBE Company;

 

ALTER TABLE Company 
MODIFY Capitalization BIGINT NOT NULL CHECK (Capitalization > 0);


ALTER TABLE Company
MODIFY CEO VARCHAR(200) NULL CHECK (CEO REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż &-.,;:]+$' OR CEO IS NULL);



-- First, drop the old check constraint on City
ALTER TABLE Company
DROP CHECK Company_chk_10;

-- Then, add a new one that is more permissive (and UTF-8 safe)
ALTER TABLE Company
ADD CONSTRAINT chk_city
CHECK (City REGEXP '^[[:alpha:]ĄąĆćĘęŁłŃńÓóŚśŹźŻż .,&;:-]+$');


ALTER TABLE Company
DROP CHECK Company_chk_7;

ALTER TABLE Company
ADD CONSTRAINT chk_city
CHECK (City REGEXP '^[A-Za-z0-9 .,&;:()-]+$');


ALTER TABLE Company
DROP CHECK Company_chk_1;

ALTER TABLE Company
ADD CONSTRAINT chk_identifier
CHECK (Identifier REGEXP '^[A-Za-z0-9 .]+$');


SHOW VARIABLES LIKE 'secure_file_priv';

SELECT *
INTO OUTFILE '/var/lib/mysql-files/company_export.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM Company;

secure-file-priv=""