CREATE DATABASE data_bank;

USE data_bank;

CREATE TABLE regions (
    region_id INTEGER,
    region_name VARCHAR(9)
);

INSERT INTO
    regions (region_id, region_name)
VALUES ('1', 'Australia'),
    ('2', 'America'),
    ('3', 'Africa'),
    ('4', 'Asia'),
    ('5', 'Europe');

CREATE TABLE customer_nodes (
    customer_id INTEGER,
    region_id INTEGER,
    node_id INTEGER,
    start_date DATE,
    end_date DATE
);

BULK INSERT customer_nodes
FROM '/tmp/customer_nodes.csv'
WITH (
        FIELDTERMINATOR = ',', -- CSV comma separation
        ROWTERMINATOR = '\n', -- Newline separation
        FIRSTROW = 2, -- Skip the header/column names row
        TABLOCK -- Minimizes log space and speeds it up
    );

CREATE TABLE customer_transactions (
    customer_id INTEGER,
    txn_date DATE,
    txn_type VARCHAR(10),
    txn_amount INTEGER
);

BULK INSERT customer_transactions
FROM '/tmp/customer_transactions.csv'
WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        FIRSTROW = 2,
        TABLOCK
    );

SELECT * FROM regions;

SELECT * FROM customer_nodes;

SELECT * FROM customer_transactions;

-----------------------------------------A. Customer Nodes Exploration----------------------------------------------
-- How many unique nodes are there on the Data Bank system ?
SELECT COUNT(DISTINCT node_id) AS unique_nodes FROM customer_nodes;

-- What is the number of nodes per region ?
SELECT r.region_name, r.region_id, COUNT(node_id) AS no_of_nodes
FROM regions r
    INNER JOIN customer_nodes cn ON r.region_id = cn.region_id
GROUP BY
    r.region_id,
    r.region_name;

-- How many customers are allocated to each region ?
SELECT r.region_name, COUNT(DISTINCT cn.customer_id) AS customer_count
FROM customer_nodes cn
    INNER JOIN regions r ON r.region_id = cn.region_id
GROUP BY
    r.region_name;

-- How many days on average are customers reallocated to a different node ?

-- What is the median, 80th and 95th percentile for this same reallocation days metric for each region ?

-----------------------------------------B. Customer Transaction----------------------------------------------
-- What is the unique count and total amount for each transaction type?
SELECT
    txn_type,
    COUNT(txn_type) AS unique_count,
    SUM(txn_amount) AS total_amount
FROM customer_transactions
GROUP BY
    txn_type;
-- What is the average total historical deposit counts and amounts for all customers?
SELECT
    AVG(deposit_count) AS avg_deposit_count,
    AVG(total_deposit) AS avg_deposit_amount
FROM (
        SELECT
            customer_id, COUNT(*) AS deposit_count, SUM(txn_amount) AS total_deposit
        FROM customer_transactions
        WHERE
            txn_type = 'deposit'
        GROUP BY
            customer_id
    ) t;

-- For each month - how many Data Bank customers make more than 1 deposit and either 1 purchase or 1 withdrawal in a single month?

-- What is the closing balance for each customer at the end of the month?

-- What is the percentage of customers who increase their closing balance by more than 5%?