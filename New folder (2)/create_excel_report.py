import pandas as pd
from ecommerce_analysis import EcommerceAnalyzer
from datetime import datetime

def create_excel_report():
    # Initialize analyzer
    analyzer = EcommerceAnalyzer('data/ecommerce_data.csv')
    analyzer.clean_data()

    # Create Excel writer object
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_file = f'ecommerce_analysis_{timestamp}.xlsx'
    
    # Create a dictionary to store all DataFrames
    sheets = {}
    
    # 1. Overview Sheet
    overview_data = {
        'Metric': [
            'Total Orders',
            'Total Revenue (₹)',
            'Average Order Value (₹)',
            'Total Customers',
            'Repeat Customers'
        ],
        'Value': [
            analyzer.df.shape[0],
            analyzer.df['total_price'].sum(),
            analyzer.df['total_price'].mean(),
            analyzer.df['customer_id'].nunique(),
            len(analyzer.df[analyzer.df.duplicated(subset=['customer_id'], keep=False)]['customer_id'].unique())
        ]
    }
    sheets['Overview'] = pd.DataFrame(overview_data)

    # 2. Product Analysis
    sheets['Product Analysis'] = analyzer.analyze_top_products()

    # 3. Regional Analysis
    sheets['Regional Analysis'] = analyzer.analyze_regional_performance()

    # 4. Payment Analysis
    sheets['Payment Analysis'] = analyzer.analyze_payment_methods()

    # 5. Customer Behavior
    customer_behavior = analyzer.analyze_customer_behavior()
    purchase_freq = pd.DataFrame(customer_behavior['purchase_frequency'].describe())
    purchase_freq.columns = ['Purchase Frequency Stats']
    sheets['Customer Behavior'] = purchase_freq

    # Write all sheets to Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name)

    print(f"Excel report has been generated: {excel_file}")

if __name__ == "__main__":
    create_excel_report() 