import json
import logging

class Visualizer:
    def generate_chart_data(self, recommendations, customer_id, products_df):
        """Generate data for Chart.js visualization with multiple datasets"""
        try:
            if not recommendations:
                logging.error("No recommendations provided for chart data")
                raise ValueError("No recommendations provided")

            # Normalize data for radar chart
            def normalize(data, min_val, max_val):
                return [(x - min_val) / (max_val - min_val) if max_val != min_val else 0.5 for x in data]

            scores = [rec['score'] for rec in recommendations]
            premiums = [
                float(products_df[products_df['product_name'] == rec['product_name']]['premium'].iloc[0]) * 12
                if not products_df[products_df['product_name'] == rec['product_name']].empty
                else 0
                for rec in recommendations
            ]
            coverages = [
                float(products_df[products_df['product_name'] == rec['product_name']]['coverage_limit'].iloc[0]) / 100000
                if not products_df[products_df['product_name'] == rec['product_name']].empty
                else 0
                for rec in recommendations
            ]
            risk_level_map = {'Low': 0.33, 'Medium': 0.66, 'High': 1.0}
            risks = [
                risk_level_map.get(products_df[products_df['product_name'] == rec['product_name']]['risk_level'].iloc[0], 0)
                if not products_df[products_df['product_name'] == rec['product_name']].empty
                else 0
                for rec in recommendations
            ]

            # Normalize for radar chart
            scores_normalized = normalize(scores, min(scores), max(scores))
            premiums_normalized = normalize(premiums, min(premiums), max(premiums))
            coverages_normalized = normalize(coverages, min(coverages), max(coverages))
            risks_normalized = normalize(risks, min(risks), max(risks))

            chart_data = {
                'labels': [rec['product_name'] for rec in recommendations],
                'datasets': [
                    {
                        'label': 'Recommendation Scores',
                        'data': scores_normalized,
                        'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Annual Premium ($)',
                        'data': premiums_normalized,
                        'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Coverage Limit ($100K)',
                        'data': coverages_normalized,
                        'backgroundColor': 'rgba(255, 206, 86, 0.5)',
                        'borderColor': 'rgba(255, 206, 86, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Risk Level',
                        'data': risks_normalized,
                        'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
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