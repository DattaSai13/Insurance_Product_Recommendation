import pandas as pd
from sklearn.preprocessing import StandardScaler
import logging

class Preprocessor:
    def preprocess(self, customers_df, products_df):
        try:
            # Handle missing values
            customers_df = customers_df.fillna({
                'income': customers_df['income'].mean(),
                'health_condition': 'Average',
                'risk_tolerance': 'Medium',
                'recent_life_event': 'None'
            })
            products_df = products_df.fillna({
                'premium': products_df['premium'].mean(),
                'risk_level': 'Medium',
                'coverage_limit': products_df['coverage_limit'].mean()
            })

            # Encode categorical variables consistently
            customers_df['marital_status'] = customers_df['marital_status'].map({
                'Single': 0, 'Married': 1, 'Divorced': 2
            })
            customers_df['health_condition'] = customers_df['health_condition'].map({
                'Good': 0, 'Average': 1, 'Poor': 2
            })
            customers_df['risk_tolerance'] = customers_df['risk_tolerance'].map({
                'Low': 0, 'Medium': 1, 'High': 2
            })
            products_df['risk_level'] = products_df['risk_level'].map({
                'Low': 0, 'Medium': 1, 'High': 2
            })
            # Keep coverage_type as strings to match needs_assessor
            products_df['coverage_type'] = products_df['coverage_type'].astype(str)

            # Scale numerical features
            scaler = StandardScaler()
            customers_df[['age', 'income']] = scaler.fit_transform(customers_df[['age', 'income']])
            products_df[['premium', 'coverage_limit']] = scaler.fit_transform(products_df[['premium', 'coverage_limit']])

            logging.debug("Data preprocessing completed")
            return customers_df, products_df
        except Exception as e:
            logging.error(f"Error in preprocessing: {str(e)}")
            raise