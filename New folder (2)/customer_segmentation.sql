-- Create a view for customer segmentation
CREATE VIEW customer_segments AS
SELECT 
    customer_id,
    customer_name,
    SUM(total_price) AS total_spent,
    COUNT(DISTINCT order_id) AS total_orders,
    AVG(total_price) AS average_order_value,
    MAX(order_date) AS last_purchase_date,
    CASE
        WHEN SUM(total_price) > 1000 THEN 'High Value'
        WHEN SUM(total_price) > 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM orders
GROUP BY customer_id, customer_name
ORDER BY total_spent DESC;

-- Query to get high-value customers
SELECT 
    customer_id,
    customer_name,
    total_spent,
    total_orders,
    average_order_value,
    last_purchase_date
FROM customer_segments
WHERE customer_segment = 'High Value'
ORDER BY total_spent DESC;

-- Query to analyze customer purchase frequency
SELECT 
    customer_segment,
    COUNT(*) AS number_of_customers,
    AVG(total_orders) AS avg_orders_per_customer,
    AVG(total_spent) AS avg_spent_per_customer
FROM customer_segments
GROUP BY customer_segment
ORDER BY avg_spent_per_customer DESC; 