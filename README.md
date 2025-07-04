Insurance Recommender
The Insurance Recommender is a web-based application designed to provide personalized insurance product recommendations based on customer profiles. It uses a Flask backend to process customer data, assess needs, and generate recommendations, and a Streamlit frontend to display interactive visualizations, including a table, bar chart, radar chart, and pie chart for recommendation scores, premiums, coverage limits, and risk levels.
Features

Personalized Recommendations: Matches insurance products to customers based on age, income, marital status, health condition, risk tolerance, and life stage.
Interactive Visualizations: Displays recommendations via:
Table: Product names, scores, premiums, coverage, risk levels, and explanations.
Bar Chart: Compares recommendation scores, premiums, coverage, and risk levels.
Radar Chart: Visualizes product comparisons across multiple metrics.
Pie Chart: Shows the distribution of recommendation scores.


Robust Backend: Flask API processes data using pandas, scikit-learn, and custom logic for life stage analysis and needs assessment.
Error Handling: Includes retry logic and detailed error messages for robust user experience.

Project Structure
InsuranceRecommender/
├── data/
│   ├── customers.csv       # Customer data (15 records)
│   └── products.csv        # Insurance product data (8 records)
├── src/
│   ├── __init__.py         # Empty file
│   ├── data_loader.py      # Loads CSV data
│   ├── preprocessor.py     # Preprocesses data
│   ├── life_stage_analyzer.py # Analyzes customer life stage
│   ├── needs_assessor.py   # Assesses customer needs
│   ├── recommender.py      # Generates recommendations
│   ├── visualizer.py       # Generates chart data
├── static/
│   ├── styles.css          # CSS for Streamlit
│   └── favicon.ico         # Favicon for Flask
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── app.py                  # Flask backend
├── streamlit_app.py        # Streamlit frontend

Installation

Clone the Repository:
git clone <repository-url>
cd InsuranceRecommender


Set Up Virtual Environment:
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac


Install Dependencies:
pip install -r requirements.txt


Ensure Data Files:

Verify data/customers.csv and data/products.csv exist in the data/ directory.



Usage

Run Flask Backend:
python app.py


The Flask server runs at http://127.0.0.1:5000.
Access http://127.0.0.1:5000/api/recommend with a POST request (e.g., {"customer_id": 1}) for recommendations.


Run Streamlit Frontend:
streamlit run streamlit_app.py


Open http://localhost:8501 in a browser.
Enter a customer ID (1–15) and click "Get Recommendations" to view:
A table with product details and explanations.
Bar, radar, and pie charts visualizing recommendation metrics.




Example API Call:
curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 1}' http://127.0.0.1:5000/api/recommend



Dependencies

Python 3.8+
Flask
Streamlit
pandas
scikit-learn
requests
Full list in requirements.txt

Troubleshooting

Connection Errors:
Ensure Flask is running before Streamlit.
Check port 5000 availability:netstat -a -n -o | find "5000"


Kill conflicting processes: taskkill /PID <pid> /F.


Allow port 5000 in firewall:netsh advfirewall firewall add rule name="Flask 5000" dir=in action=allow protocol=TCP localport=5000




Missing Data:
Verify data/customers.csv and data/products.csv are present.


Visualization Issues:
Check browser console (F12 > Console) for JavaScript errors.
Ensure Flask API returns valid JSON.



Contributing
Contributions are welcome! Please submit pull requests or open issues for bugs, features, or improvements.
