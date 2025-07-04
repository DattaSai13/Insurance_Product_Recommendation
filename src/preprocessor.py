from sklearn.preprocessing import StandardScaler
import pandas as pd
import logging

class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def preprocess(self, customers_df, products_df):
        """Preprocess customer and product data"""
        try:
            # Encode categorical variables
            customers_df['marital_status_code'] = customers_df['marital_status'].map({
                'Single': 0, 'Married': 1, 'Divorced': 2
            })
            customers_df['health_condition_code'] = customers_df['health_condition'].map({
                'Good': 2, 'Average': 1, 'Poor': 0
            })
            customers_df['risk_tolerance_code'] = customers_df['risk_tolerance'].map({
                'High': 2, 'Medium': 1, 'Low': 0
            })
            customers_df['life_event_code'] = customers_df['recent_life_event'].map({
                'None': 0, 'Marriage': 1, 'New Child': 2, 'Job Change': 3, 'Retirement': 4
            })

            # Scale numerical features
            numerical_features = ['age', 'income']
            customers_df[numerical_features] = self.scaler.fit_transform(customers_df[numerical_features])
            
            logging.info("Data preprocessing completed")
            return customers_df, products_df
        except Exception as e:
            logging.error(f"Error in preprocessing: {e}")
            raise