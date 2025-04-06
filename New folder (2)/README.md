# E-Commerce Sales Analysis Project

This project provides a comprehensive analysis of e-commerce sales data, including data cleaning, exploratory data analysis, customer segmentation, and visualization.

## Project Structure

```
.
├── data/                   # Directory for storing the dataset
├── visualizations/         # Directory for storing generated visualizations
├── ecommerce_analysis.py   # Main Python script for analysis
├── customer_segmentation.sql # SQL queries for customer analysis
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Place your e-commerce dataset in the `data` directory as `ecommerce_data.csv`

3. Run the analysis:
```bash
python ecommerce_analysis.py
```

## Features

- Data cleaning and preprocessing
- Top product analysis
- Revenue trend analysis
- Peak sales period identification
- Customer segmentation
- Interactive visualizations

## Data Requirements

The dataset should include the following columns:
- order_id
- customer_id
- customer_name
- product_name
- quantity
- total_price
- order_date

## Output

The analysis will generate:
1. Visualizations in the `visualizations` directory
2. A comprehensive report with key metrics
3. Customer segmentation analysis

## SQL Analysis

The `customer_segmentation.sql` file contains queries for:
- Creating customer segments based on spending
- Identifying high-value customers
- Analyzing purchase frequency

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request 