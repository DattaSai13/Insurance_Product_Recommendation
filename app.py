from flask import Flask, request, render_template, send_from_directory, jsonify
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.life_stage_analyzer import LifeStageAnalyzer
from src.needs_assessor import NeedsAssessor
from src.recommender import Recommender
from src.visualizer import Visualizer
import logging
import json
import os
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    logging.debug("Serving index.html (legacy)")
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    logging.debug("Received request to /api/recommend")
    try:
        # Verify file existence
        for file_path in ['data/customers.csv', 'data/products.csv']:
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}")
                return jsonify({'error': f'File not found: {file_path}'}), 500

        data_loader = DataLoader('data/customers.csv', 'data/products.csv')
        preprocessor = Preprocessor()
        life_stage_analyzer = LifeStageAnalyzer()
        visualizer = Visualizer()

        logging.debug("Loading data")
        customers_df, products_df = data_loader.load_data()
        logging.debug(f"Customers shape: {customers_df.shape}, Products shape: {products_df.shape}")

        logging.debug("Preprocessing data")
        customers_df, products_df = preprocessor.preprocess(customers_df, products_df)
        logging.debug(f"Preprocessed customers: {customers_df.head().to_dict()}")
        logging.debug(f"Preprocessed products: {products_df.head().to_dict()}")

        logging.debug("Initializing needs assessor and recommender")
        needs_assessor = NeedsAssessor(products_df=products_df)
        recommender = Recommender(customers_df=customers_df, products_df=products_df)
        recommender.set_dependencies(life_stage_analyzer, needs_assessor)

        # Get customer ID from JSON payload
        data = request.get_json()
        if not data or 'customer_id' not in data:
            logging.error("Missing customer_id in request")
            return jsonify({'error': 'Missing customer_id in request'}), 400

        customer_id = data.get('customer_id')
        logging.debug(f"Request data: {data}")
        if not isinstance(customer_id, int) or customer_id < 1 or customer_id > 15:
            logging.error(f"Invalid customer ID: {customer_id}")
            return jsonify({'error': 'Invalid customer ID. Must be between 1 and 15.'}), 400

        logging.debug(f"Processing customer ID: {customer_id}")
        customer = customers_df[customers_df['customer_id'] == customer_id]
        if customer.empty:
            logging.error(f"Customer ID {customer_id} not found in data")
            return jsonify({'error': f'Customer ID {customer_id} not found'}), 404

        customer = customer.iloc[0]
        logging.debug(f"Customer data: {customer.to_dict()}")
        life_stage, life_event_weight = life_stage_analyzer.analyze(customer, customer_id)
        logging.debug(f"Life stage: {life_stage}, Weight: {life_event_weight}")
        needs = needs_assessor.assess(customer, customer_id, life_stage)
        logging.debug(f"Needs: {needs}")
        recommendations = recommender.get_recommendations(customer_id, needs, life_stage, life_event_weight)
        if not recommendations:
            logging.error(f"No recommendations generated for customer {customer_id}. Needs: {needs}, Products coverage: {products_df['coverage_type'].unique()}")
            return jsonify({'error': f'No recommendations generated for customer {customer_id}'}), 500
        logging.debug(f"Recommendations: {recommendations}")
        chart_data = visualizer.generate_chart_data(recommendations, customer_id, products_df)
        logging.debug(f"Chart data: {chart_data}")

        return jsonify({
            'customer_id': customer_id,
            'recommendations': recommendations,
            'chart_data': chart_data
        })
    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
        return jsonify({'error': f'File not found: {str(e)}'}), 500
    except ValueError as e:
        logging.error(f"Data validation error: {str(e)}")
        return jsonify({'error': f'Data validation error: {str(e)}'}), 500
    except Exception as e:
        logging.error(f"Server error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == "__main__":
    # Bind to 0.0.0.0 to ensure accessibility
    app.run(debug=True, host='0.0.0.0', port=5000)