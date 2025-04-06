import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class EcommerceAnalyzer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Load the e-commerce dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print("Data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def clean_data(self):
        """Clean the dataset"""
        if self.df is None:
            return
            
        # Convert date column to datetime
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        
        # Add derived columns
        self.df['month'] = self.df['order_date'].dt.to_period('M')
        self.df['day_of_week'] = self.df['order_date'].dt.day_name()
        self.df['hour'] = self.df['order_date'].dt.hour
        
        print("Data cleaning completed!")
        
    def analyze_top_products(self):
        """Analyze top selling products"""
        if self.df is None:
            return
            
        # Product revenue analysis
        product_revenue = self.df.groupby('product_name').agg({
            'total_price': 'sum',
            'quantity': 'sum',
            'order_id': 'count'
        }).round(2)
        
        product_revenue.columns = ['Total Revenue (₹)', 'Units Sold', 'Number of Orders']
        product_revenue = product_revenue.sort_values('Total Revenue (₹)', ascending=False)
        
        return product_revenue
        
    def analyze_revenue_trends(self):
        """Analyze revenue trends over time"""
        if self.df is None:
            return
            
        # Monthly revenue trends
        monthly_revenue = self.df.groupby('month')['total_price'].sum()
        
        # Calculate month-over-month growth
        monthly_growth = monthly_revenue.pct_change() * 100
        
        return {
            'revenue': monthly_revenue,
            'growth': monthly_growth
        }
        
    def analyze_regional_performance(self):
        """Analyze sales performance by region"""
        if self.df is None:
            return
            
        # City-wise analysis
        city_metrics = self.df.groupby('city').agg({
            'total_price': ['sum', 'mean', 'count'],
            'order_id': 'count'
        }).round(2)
        
        city_metrics.columns = ['Total Revenue (₹)', 'Avg Order Value (₹)', 
                              'Number of Transactions', 'Number of Orders']
        return city_metrics.sort_values('Total Revenue (₹)', ascending=False)
        
    def analyze_payment_methods(self):
        """Analyze payment method preferences"""
        if self.df is None:
            return
            
        payment_analysis = self.df.groupby('payment_method').agg({
            'order_id': 'count',
            'total_price': ['sum', 'mean']
        }).round(2)
        
        payment_analysis.columns = ['Number of Orders', 'Total Revenue (₹)', 'Avg Order Value (₹)']
        return payment_analysis.sort_values('Number of Orders', ascending=False)
        
    def analyze_customer_behavior(self):
        """Analyze customer purchasing behavior"""
        if self.df is None:
            return
            
        # Customer purchase frequency
        purchase_frequency = self.df.groupby('customer_id').size()
        
        # Average order value by customer
        avg_order_value = self.df.groupby('customer_id')['total_price'].mean()
        
        # Customer lifetime value
        customer_lifetime = self.df.groupby('customer_id')['total_price'].sum()
        
        # Customer city preference
        customer_cities = self.df.groupby('customer_id')['city'].agg(lambda x: x.value_counts().index[0])
        
        # Preferred payment methods
        customer_payments = self.df.groupby('customer_id')['payment_method'].agg(lambda x: x.value_counts().index[0])
        
        return {
            'purchase_frequency': purchase_frequency.describe(),
            'avg_order_value': avg_order_value.describe(),
            'customer_lifetime': customer_lifetime.describe(),
            'city_distribution': customer_cities.value_counts(),
            'payment_preferences': customer_payments.value_counts()
        }
        
    def create_visualizations(self):
        """Create visualizations for the analysis"""
        if self.df is None:
            return
            
        # Set style
        plt.style.use('default')
        sns.set_style("whitegrid")
        
        # Create directory for visualizations
        os.makedirs('visualizations', exist_ok=True)
        
        # 1. Top Products Visualization
        plt.figure(figsize=(12, 6))
        top_products = self.analyze_top_products()
        sns.barplot(x=top_products.index, y=top_products['Total Revenue (₹)'])
        plt.title('Category-wise Revenue Distribution')
        plt.xlabel('Product Category')
        plt.ylabel('Revenue (₹)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/category_revenue.png')
        plt.close()
        
        # 2. Revenue Trends Visualization
        trends = self.analyze_revenue_trends()
        plt.figure(figsize=(12, 6))
        trends['revenue'].plot(kind='line', marker='o')
        plt.title('Monthly Revenue Trends')
        plt.xlabel('Month')
        plt.ylabel('Revenue (₹)')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('visualizations/revenue_trends.png')
        plt.close()
        
        # 3. Regional Performance
        plt.figure(figsize=(12, 6))
        city_metrics = self.analyze_regional_performance()
        sns.barplot(x=city_metrics.index, y=city_metrics['Total Revenue (₹)'])
        plt.title('City-wise Revenue Distribution')
        plt.xlabel('City')
        plt.ylabel('Revenue (₹)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/city_revenue.png')
        plt.close()
        
        # 4. Payment Methods Analysis
        plt.figure(figsize=(10, 6))
        payment_data = self.analyze_payment_methods()
        sns.barplot(x=payment_data.index, y=payment_data['Number of Orders'])
        plt.title('Payment Method Distribution')
        plt.xlabel('Payment Method')
        plt.ylabel('Number of Orders')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/payment_methods.png')
        plt.close()
        
        print("Visualizations created successfully!")
        
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        if self.df is None:
            return
            
        # Basic metrics
        total_orders = len(self.df)
        total_revenue = self.df['total_price'].sum()
        avg_order_value = self.df['total_price'].mean()
        
        # Customer metrics
        total_customers = self.df['customer_id'].nunique()
        repeat_customers = self.df.groupby('customer_id').size()[lambda x: x > 1].count()
        
        # Product metrics
        product_analysis = self.analyze_top_products()
        
        # Regional metrics
        regional_analysis = self.analyze_regional_performance()
        
        # Payment analysis
        payment_analysis = self.analyze_payment_methods()
        
        # Customer behavior
        customer_behavior = self.analyze_customer_behavior()
        
        report = {
            'overview': {
                'total_orders': total_orders,
                'total_revenue': f"₹{total_revenue:,.2f}",
                'average_order_value': f"₹{avg_order_value:,.2f}",
                'total_customers': total_customers,
                'repeat_customers': repeat_customers
            },
            'product_analysis': product_analysis.to_dict(),
            'regional_analysis': regional_analysis.to_dict(),
            'payment_analysis': payment_analysis.to_dict(),
            'customer_behavior': customer_behavior
        }
        
        return report

if __name__ == "__main__":
    # Generate sample data first
    import generate_sample_data
    generate_sample_data.generate_sample_data()
    
    # Run analysis
    analyzer = EcommerceAnalyzer('data/ecommerce_data.csv')
    analyzer.clean_data()
    analyzer.create_visualizations()
    report = analyzer.generate_report()
    
    # Print formatted report
    print("\nE-commerce Analysis Report (Indian Market)")
    print("=" * 50)
    
    print("\n1. Overview:")
    for key, value in report['overview'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n2. Top Product Categories:")
    product_df = pd.DataFrame(report['product_analysis'])
    print(product_df.head().to_string())
    
    print("\n3. Top Performing Cities:")
    city_df = pd.DataFrame(report['regional_analysis'])
    print(city_df.head().to_string())
    
    print("\n4. Payment Method Analysis:")
    payment_df = pd.DataFrame(report['payment_analysis'])
    print(payment_df.to_string())
    
    print("\n5. Customer Behavior Insights:")
    print("\nPurchase Frequency:")
    for stat, value in report['customer_behavior']['purchase_frequency'].items():
        print(f"  {stat}: {value:,.2f}")
        
    print("\nCustomer City Distribution (Top 5):")
    for city, count in report['customer_behavior']['city_distribution'].head().items():
        print(f"  {city}: {count:,}") 