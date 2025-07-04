import logging

class LifeStageAnalyzer:
    def analyze(self, customer, customer_id):
        """Analyze customer's life stage and life events"""
        try:
            age = customer['age']
            marital_status = customer['marital_status']
            has_children = customer['has_children']
            recent_life_event = customer['recent_life_event']
            
            if age < 25 and marital_status == 'Single':
                life_stage = 'Student/Young Single'
            elif age < 30 and marital_status == 'Single':
                life_stage = 'Young Single'
            elif age >= 30 and marital_status == 'Married' and has_children > 0:
                life_stage = 'Family'
            elif age >= 60:
                life_stage = 'Retiree'
            elif age >= 45:
                life_stage = 'Mature'
            else:
                life_stage = 'Adult'
                
            life_event_weight = 0.2 if recent_life_event != 'None' else 0
            logging.info(f"Life stage for customer {customer_id}: {life_stage}")
            return life_stage, life_event_weight
        except Exception as e:
            logging.error(f"Error in life stage analysis: {e}")
            raise