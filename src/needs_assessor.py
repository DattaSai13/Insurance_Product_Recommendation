import logging

class NeedsAssessor:
    def __init__(self, products_df):
        self.products_df = products_df

    def assess(self, customer, customer_id, life_stage):
        """Assess customer needs based on profile and profitability"""
        try:
            needs = []
            income = customer['income']
            income_mean = self.products_df['premium'].mean() * 12  # Annual premium proxy
            
            if life_stage == 'Student/Young Single':
                needs.extend(['Health Insurance', 'Disability Insurance'])
            elif life_stage == 'Family':
                needs.extend(['Term Life', 'Health Insurance', 'Critical Illness'])
            elif life_stage == 'Mature' or life_stage == 'Retiree':
                needs.extend(['Whole Life', 'Health Insurance', 'Critical Illness'])
            else:
                needs.extend(['Term Life', 'Health Insurance'])
                
            if income > income_mean:
                needs.append('Whole Life')
                
            if customer['recent_life_event'] in ['Marriage', 'New Child']:
                needs.append('Term Life')
            elif customer['recent_life_event'] == 'Job Change':
                needs.append('Disability Insurance')
            elif customer['recent_life_event'] == 'Retirement':
                needs.append('Whole Life')
                
            # Filter products by profitability (premium-to-coverage ratio)
            profitable_needs = []
            for need in set(needs):
                product = self.products_df[self.products_df['product_name'] == need]
                if not product.empty:
                    premium = product['premium'].iloc[0]
                    coverage = product['coverage_limit'].iloc[0]
                    if coverage / premium > 100:  # Arbitrary threshold for profitability
                        profitable_needs.append(need)
            
            logging.info(f"Needs for customer {customer_id}: {profitable_needs}")
            return profitable_needs
        except Exception as e:
            logging.error(f"Error in needs assessment: {e}")
            raise