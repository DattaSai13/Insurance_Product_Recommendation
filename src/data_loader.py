import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    def __init__(self, customers_file, products_file):
        self.customers_file = customers_file
        self.products_file = products_file

    def load_data(self):
        """Load and validate customer and product data"""
        try:
            customers_df = pd.read_csv(self.customers_file)
            products_df = pd.read_csv(self.products_file)
            logging.info("Data loaded successfully")
            self.validate_data(customers_df, products_df)
            return customers_df, products_df
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def validate_data(self, customers_df, products_df):
        """Validate data integrity"""
        required_customer_cols = ['customer_id', 'age', 'income', 'marital_status', 'has_children', 'health_condition', 'risk_tolerance']
        required_product_cols = ['product_id', 'product_name', 'coverage_type', 'premium', 'risk_level', 'recommended_age_min', 'recommended_age_max']
        
        if not all(col in customers_df.columns for col in required_customer_cols):
            raise ValueError("Missing required columns in customers.csv")
        if not all(col in products_df.columns for col in required_product_cols):
            raise ValueError("Missing required columns in products.csv")
        
        # Handle missing values
        customers_df['income'] = customers_df['income'].fillna(customers_df['income'].median())
        logging.info("Data validation completed")