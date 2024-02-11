CREATE TABLE IF NOT EXISTS instructions
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    'name'          VARCHAR,
    file_path       VARCHAR,
    validation_date DATE DEFAULT CURRENT_DATE,
    expiration_date DATE
);


---------------------------------------- VALIDATIONS ----------------------------------------
CREATE TABLE IF NOT EXISTS validations
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    instruction_id INTEGER,
    date           DATE DEFAULT CURRENT_DATE
);


------------------------------------------ HISTORY ------------------------------------------
CREATE TABLE IF NOT EXISTS history
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    user_code       VARCHAR,
    instruction_id INTEGER
);
