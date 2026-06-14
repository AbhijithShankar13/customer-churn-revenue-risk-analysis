-- Total Customers

SELECT COUNT(*) AS total_customers
FROM customers;

-- Churn Rate

SELECT
ROUND(
100.0 *
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)
/
COUNT(*),
2
) AS churn_rate
FROM customers;

-- Revenue by Contract

SELECT
Contract,
ROUND(SUM(MonthlyCharges),2) AS revenue
FROM customers
GROUP BY Contract;

-- Churn by Contract

SELECT
Contract,
COUNT(*) AS churned_customers
FROM customers
WHERE Churn='Yes'
GROUP BY Contract;

-- Average Monthly Charges

SELECT
AVG(MonthlyCharges)
FROM customers;