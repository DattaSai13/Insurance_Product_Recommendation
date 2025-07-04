import logging

class NeedsAssessor:
    def __init__(self, products_df):
        self.products_df = products_df

    def assess(self, customer, customer_id, life_stage):
        try:
            needs = []
            if life_stage == 'Student/Young Single':
                needs.append('Health')
                needs.append('Income')
            elif life_stage == 'Young Family':
                needs.extend(['Life', 'Health', 'Income'])
            elif life_stage == 'Mature Family':
                needs.extend(['Life', 'Health'])
            elif life_stage == 'Retirement':
                needs.extend(['Health', 'Life'])
            elif life_stage == 'Midlife Single':
                needs.extend(['Health', 'Income'])

            if customer['health_condition'] == 2:  # Poor
                needs.append('Health')
            if customer['risk_tolerance'] == 0:  # Low
                needs.append('Life')

            needs = list(set(needs))  # Remove duplicates
            logging.debug(f"Customer {customer_id} needs: {needs}")
            return needs
        except Exception as e:
            logging.error(f"Error in needs assessment: {str(e)}")
            raise