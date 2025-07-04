import logging

class LifeStageAnalyzer:
    def analyze(self, customer, customer_id):
        try:
            age = customer['age']
            marital_status = customer['marital_status']
            has_children = customer['has_children']
            recent_life_event = customer['recent_life_event']

            if age < 30 and marital_status == 0 and has_children == 0:
                life_stage = 'Student/Young Single'
            elif 30 <= age <= 45 and marital_status == 1 and has_children > 0:
                life_stage = 'Young Family'
            elif age > 45 and marital_status == 1:
                life_stage = 'Mature Family'
            elif age >= 60:
                life_stage = 'Retirement'
            else:
                life_stage = 'Midlife Single'

            life_event_weight = 1.0
            if recent_life_event in ['New Child', 'Marriage', 'Job Change']:
                life_event_weight = 1.2
            elif recent_life_event == 'Retirement':
                life_event_weight = 1.5

            logging.debug(f"Customer {customer_id} life stage: {life_stage}, weight: {life_event_weight}")
            return life_stage, life_event_weight
        except Exception as e:
            logging.error(f"Error in life stage analysis: {str(e)}")
            raise