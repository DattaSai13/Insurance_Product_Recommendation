import pandas as pd
import logging
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Recommender:
    def __init__(self, customers_df, products_df):
        self.customers_df = customers_df
        self.products_df = products_df
        self.life_stage_analyzer = None
        self.needs_assessor = None

    def set_dependencies(self, life_stage_analyzer, needs_assessor):
        self.life_stage_analyzer = life_stage_analyzer
        self.needs_assessor = needs_assessor

    def calculate_similarity(self, customer, product):
        try:
            customer_features = np.array([
                customer['age'],
                customer['income'],
                customer['marital_status'],
                customer['has_children'],
                customer['health_condition'],
                customer['risk_tolerance']
            ]).reshape(1, -1)
            product_features = np.array([
                (product['recommended_age_min'] + product['recommended_age_max']) / 2,
                product['premium'],
                0,  # Placeholder for marital_status
                0,  # Placeholder for has_children
                product['risk_level'],
                product['risk_level']
            ]).reshape(1, -1)
            similarity = cosine_similarity(customer_features, product_features)[0][0]
            return max(0.1, min(similarity, 1.0))  # Ensure score is positive and capped
        except Exception as e:
            logging.error(f"Error in similarity calculation: {str(e)}")
            raise

    def get_recommendations(self, customer_id, needs, life_stage, life_event_weight):
        try:
            customer = self.customers_df[self.customers_df['customer_id'] == customer_id].iloc[0]
            recommendations = []
            logging.debug(f"Customer {customer_id} needs: {needs}, Available coverage types: {self.products_df['coverage_type'].unique()}")
            for _, product in self.products_df.iterrows():
                if str(product['coverage_type']) in needs:
                    score = self.calculate_similarity(customer, product) * life_event_weight
                    explanation = f"Recommended for {life_stage} life stage, matches {product['coverage_type']} need"
                    recommendations.append({
                        'product_id': int(product['product_id']),
                        'product_name': product['product_name'],
                        'score': float(score),
                        'explanation': explanation
                    })
                else:
                    logging.debug(f"Skipping product {product['product_name']} as coverage_type {product['coverage_type']} not in needs {needs}")
            if not recommendations:
                logging.warning(f"No products matched needs {needs} for customer {customer_id}")
                # Fallback: Recommend top products
                for _, product in self.products_df.iterrows():
                    score = self.calculate_similarity(customer, product) * life_event_weight * 0.8
                    explanation = f"Fallback recommendation for {life_stage} life stage"
                    recommendations.append({
                        'product_id': int(product['product_id']),
                        'product_name': product['product_name'],
                        'score': float(score),
                        'explanation': explanation
                    })
            recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)[:3]
            logging.debug(f"Recommendations for customer {customer_id}: {recommendations}")
            return recommendations
        except Exception as e:
            logging.error(f"Error in getting recommendations: {str(e)}")
            raise