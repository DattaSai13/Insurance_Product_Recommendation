import pandas as pd
import logging

class DataLoader:
    def __init__(self, customers_file, products_file):
        self.customers_file = customers_file
        self.products_file = products_file

    def load_data(self):
        try:
            customers_df = pd.read_csv(self.customers_file)
            products_df = pd.read_csv(self.products_file)
            logging.debug(f"Loaded customers: {customers_df.shape}, products: {products_df.shape}")
            return customers_df, products_df
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            raise