import json
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.life_stage_analyzer import LifeStageAnalyzer
from src.needs_assessor import NeedsAssessor
from src.recommender import Recommender
from src.visualizer import Visualizer

def main():
    # Initialize components
    data_loader = DataLoader('data/customers.csv', 'data/products.csv')
    preprocessor = Preprocessor()
    life_stage_analyzer = LifeStageAnalyzer()
    visualizer = Visualizer()

    # Load and preprocess data first
    customers_df, products_df = data_loader.load_data()
    customers_df, products_df = preprocessor.preprocess(customers_df, products_df)
    
    # Initialize needs assessor and recommender with loaded data
    needs_assessor = NeedsAssessor(products_df=products_df)
    recommender = Recommender(customers_df=customers_df, products_df=products_df)
    recommender.set_dependencies(life_stage_analyzer, needs_assessor)

    # Generate recommendations for customer ID 1
    customer_id = 1
    customer = customers_df[customers_df['customer_id'] == customer_id].iloc[0]
    life_stage, life_event_weight = life_stage_analyzer.analyze(customer, customer_id)
    needs = needs_assessor.assess(customer, customer_id, life_stage)
    recommendations = recommender.get_recommendations(customer_id, needs, life_stage, life_event_weight)
    
    # Save and print results
    result = {'customer_id': customer_id, 'recommendations': recommendations}
    with open('recommendations.json', 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    
    # Generate visualization
    visualizer.generate_chart_data(recommendations, customer_id)

if __name__ == "__main__":
    main()