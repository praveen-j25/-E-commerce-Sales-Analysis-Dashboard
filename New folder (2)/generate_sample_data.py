import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records=1000):
    # Generate random dates
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days
    
    # Sample product categories based on popular Flipkart categories
    categories = [
        'Mobile Phones',
        'Fashion',
        'Electronics',
        'Home & Kitchen',
        'Grocery & Staples',
        'Beauty & Personal Care',
        'Books & Stationery',
        'Sports & Fitness',
        'Furniture',
        'Appliances'
    ]
    
    # Sample cities for delivery
    cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
        'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'
    ]
    
    # Price ranges for different categories (in INR)
    category_price_ranges = {
        'Mobile Phones': (8000, 50000),
        'Fashion': (500, 5000),
        'Electronics': (1000, 80000),
        'Home & Kitchen': (500, 15000),
        'Grocery & Staples': (200, 3000),
        'Beauty & Personal Care': (100, 2000),
        'Books & Stationery': (200, 1500),
        'Sports & Fitness': (500, 10000),
        'Furniture': (2000, 50000),
        'Appliances': (5000, 80000)
    }
    
    # Generate sample data
    data = []
    for i in range(1, num_records + 1):
        # Select random category
        category = random.choice(categories)
        # Get price range for category
        min_price, max_price = category_price_ranges[category]
        
        # Generate order
        order = {
            'order_id': f'OD{i:06d}',
            'customer_id': f'CUST{random.randint(1, num_records//2):04d}',  # Creating repeat customers
            'customer_name': f'Customer {random.randint(1, num_records//2)}',
            'product_name': category,
            'quantity': np.random.randint(1, 5),
            'city': random.choice(cities),
            'payment_method': random.choice(['UPI', 'Credit Card', 'Debit Card', 'COD', 'Net Banking']),
            'order_date': start_date + timedelta(days=random.randint(0, date_range))
        }
        
        # Calculate total price based on category and quantity
        base_price = round(np.random.uniform(min_price, max_price), -1)  # Round to nearest 10
        order['total_price'] = base_price * order['quantity']
        
        # Add festival season discounts (October-November)
        order_month = order['order_date'].month
        if order_month in [10, 11]:  # Diwali season
            order['total_price'] = order['total_price'] * 0.8  # 20% discount
        
        data.append(order)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by date
    df = df.sort_values('order_date')
    
    # Save to CSV
    df.to_csv('data/ecommerce_data.csv', index=False)
    print(f"Generated {num_records} sample records in data/ecommerce_data.csv")

if __name__ == "__main__":
    generate_sample_data() 