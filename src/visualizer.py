import json
import logging

class Visualizer:
    def generate_chart_data(self, recommendations, customer_id, products_df):
        """Generate data for Chart.js visualization with multiple datasets"""
        try:
            if not recommendations:
                logging.error("No recommendations provided for chart data")
                raise ValueError("No recommendations provided")

            # Create datasets for recommendation scores, premiums, and coverage limits
            chart_data = {
                'labels': [rec['product_name'] for rec in recommendations],
                'datasets': [
                    {
                        'label': 'Recommendation Scores',
                        'data': [rec['score'] for rec in recommendations],
                        'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Annual Premium ($)',
                        'data': [
                            float(products_df[products_df['product_name'] == rec['product_name']]['premium'].iloc[0]) * 12
                            if not products_df[products_df['product_name'] == rec['product_name']].empty
                            else 0
                            for rec in recommendations
                        ],
                        'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Coverage Limit ($100K)',
                        'data': [
                            float(products_df[products_df['product_name'] == rec['product_name']]['coverage_limit'].iloc[0]) / 100000
                            if not products_df[products_df['product_name'] == rec['product_name']].empty
                            else 0
                            for rec in recommendations
                        ],
                        'backgroundColor': 'rgba(255, 206, 86, 0.5)',
                        'borderColor': 'rgba(255, 206, 86, 1)',
                        'borderWidth': 1
                    }
                ]
            }
            with open(f'static/chart_data_{customer_id}.json', 'w') as f:
                json.dump(chart_data, f, indent=2)
            logging.info(f"Chart data generated for customer {customer_id}: {chart_data}")
            return chart_data
        except Exception as e:
            logging.error(f"Error in visualization: {str(e)}")
            raise