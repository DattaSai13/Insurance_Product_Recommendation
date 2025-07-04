import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import logging

class Recommender:
    def __init__(self, customers_df, products_df):
        self.customers_df = customers_df
        self.products_df = products_df
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        # Simulate user-item interaction matrix (for collaborative filtering)
        self.user_item_matrix = self._create_user_item_matrix()

    def _create_user_item_matrix(self):
        """Simulate user-item interactions for collaborative filtering"""
        try:
            np.random.seed(42)
            matrix = np.zeros((len(self.customers_df), len(self.products_df)))
            for i in range(len(self.customers_df)):
                purchased = np.random.choice(len(self.products_df), size=2, replace=False)
                matrix[i, purchased] = 1
            return matrix
        except Exception as e:
            logging.error(f"Error creating user-item matrix: {e}")
            raise

    def calculate_similarity(self, customer_id):
        """Calculate content-based and collaborative filtering similarities"""
        try:
            customer = self.customers_df[self.customers_df['customer_id'] == customer_id].iloc[0]
            
            # Content-based: Numerical features
            customer_vector = np.array([[
                customer['age'],
                customer['income'],
                customer['marital_status_code'],
                customer['health_condition_code'],
            ]])
            
            product_vectors = []
            for _, product in self.products_df.iterrows():
                product_vector = [
                    (product['recommended_age_min'] + product['recommended_age_max']) / 2,
                    self.customers_df['income'].mean(),
                    1 if product['coverage_type'] in ['Life', 'Health'] else 0,
                    1 if product['risk_level'] == 'Medium' else 0
                ]
                product_vectors.append(product_vector)
                
            content_similarities = cosine_similarity(customer_vector, np.array(product_vectors))[0]
            
            # Content-based: Textual features (product descriptions)
            product_descriptions = self.products_df['description'].tolist()
            tfidf_matrix = self.tfidf.fit_transform(product_descriptions)
            customer_needs = ' '.join(self.needs_assessor.assess(customer, customer_id, self.life_stage_analyzer.analyze(customer, customer_id)[0]))
            customer_tfidf = self.tfidf.transform([customer_needs])
            text_similarities = cosine_similarity(customer_tfidf, tfidf_matrix)[0]
            
            # Collaborative filtering
            customer_idx = self.customers_df.index[self.customers_df['customer_id'] == customer_id].tolist()[0]
            collab_similarities = cosine_similarity([self.user_item_matrix[customer_idx]], self.user_item_matrix)[0]
            collab_scores = np.mean([self.user_item_matrix[other_idx] for other_idx in np.argsort(collab_similarities)[-3:]], axis=0)
            
            # Combine scores (60% content-based, 20% text-based, 20% collaborative)
            final_scores = 0.6 * content_similarities + 0.2 * text_similarities + 0.2 * collab_scores
            return final_scores
        except Exception as e:
            logging.error(f"Error in similarity calculation: {e}")
            raise

    def get_recommendations(self, customer_id, needs, life_stage, life_event_weight, top_n=3):
        """Generate ranked product recommendations with explanations"""
        try:
            if customer_id not in self.customers_df['customer_id'].values:
                raise ValueError(f"Customer ID {customer_id} not found")
                
            similarities = self.calculate_similarity(customer_id)
            recommendations = []
            
            for idx, product in self.products_df.iterrows():
                if product['product_name'] in needs:
                    score = similarities[idx] * (1 + life_event_weight)
                    explanation = f"Recommended for {life_stage} life stage"
                    if product['risk_level'] == self.customers_df[self.customers_df['customer_id'] == customer_id]['risk_tolerance'].iloc[0]:
                        explanation += f" and matches risk tolerance ({product['risk_level']})"
                        
                    recommendations.append({
                        'product_id': product['product_id'],
                        'product_name': product['product_name'],
                        'score': score,
                        'explanation': explanation
                    })
            
            recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)[:top_n]
            logging.info(f"Recommendations generated for customer {customer_id}")
            return recommendations
        except Exception as e:
            logging.error(f"Error in recommendation generation: {e}")
            raise

    def set_dependencies(self, life_stage_analyzer, needs_assessor):
        """Set dependencies for modular integration"""
        self.life_stage_analyzer = life_stage_analyzer
        self.needs_assessor = needs_assessor