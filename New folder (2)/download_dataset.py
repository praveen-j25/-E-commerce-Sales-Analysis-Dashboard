import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    """Download the e-commerce dataset from Kaggle"""
    try:
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()
        
        # Download the dataset
        dataset_name = "olistbr/brazilian-ecommerce"
        api.dataset_download_files(dataset_name, path='data', unzip=True)
        
        print("Dataset downloaded successfully!")
        
        # Prepare the dataset
        prepare_dataset()
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")

def prepare_dataset():
    """Prepare the dataset for analysis"""
    try:
        # Read the necessary files
        orders = pd.read_csv('data/olist_orders_dataset.csv')
        order_items = pd.read_csv('data/olist_order_items_dataset.csv')
        customers = pd.read_csv('data/olist_customers_dataset.csv')
        products = pd.read_csv('data/olist_products_dataset.csv')
        
        # Merge the datasets
        df = pd.merge(orders, order_items, on='order_id')
        df = pd.merge(df, customers, on='customer_id')
        df = pd.merge(df, products, on='product_id')
        
        # Select and rename columns
        df = df[[
            'order_id',
            'customer_id',
            'customer_unique_id',
            'product_id',
            'product_category_name',
            'price',
            'order_purchase_timestamp'
        ]]
        
        df.columns = [
            'order_id',
            'customer_id',
            'customer_name',
            'product_id',
            'product_name',
            'total_price',
            'order_date'
        ]
        
        # Save the prepared dataset
        df.to_csv('data/ecommerce_data.csv', index=False)
        print("Dataset prepared and saved successfully!")
        
    except Exception as e:
        print(f"Error preparing dataset: {e}")

if __name__ == "__main__":
    download_dataset() 