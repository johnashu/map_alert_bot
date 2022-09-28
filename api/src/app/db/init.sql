-- Database: alerts_db 

-- DROP DATABASE alerts_db;

-- CREATE TABLE table_name (
--    column_name TYPE column_constraint,
--    table_constraint table_constraint
-- ) INHERITS existing_table_name;

-- DROP DATABASE IF EXISTS alerts_db

    
CREATE DATABASE alerts_db
    WITH 
    OWNER = maffaz
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;