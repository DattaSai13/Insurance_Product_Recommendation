import streamlit as st
import requests
import json
import streamlit.components.v1 as components
import pandas as pd
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Streamlit app configuration
st.set_page_config(page_title="Insurance Recommender", page_icon=":bar_chart:", layout="wide")

# CSS for styling
st.markdown("""
    <style>
        .main { background-color: #f5f5f5; padding: 20px; }
        .error { color: red; font-weight: bold; }
        .stButton>button { background-color: #4CAF50; color: white; }
        .stNumberInput>div>input { width: 100px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Insurance Product Recommender")

# Customer ID input
customer_id = st.number_input("Enter Customer ID (1–15):", min_value=1, max_value=15, step=1)

# Function to fetch recommendations with retries
def fetch_recommendations(customer_id, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            logging.debug(f"Attempt {attempt + 1}: Sending request to http://127.0.0.1:5000/api/recommend for customer {customer_id}")
            response = requests.post(
                "http://127.0.0.1:5000/api/recommend",
                json={"customer_id": int(customer_id)},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            logging.debug(f"API response: {data}")
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                st.markdown(f'<p class="error">Connection attempt {attempt + 1} failed: {str(e)}. Retrying...</p>', unsafe_allow_html=True)
                time.sleep(delay)
            else:
                raise

# Button to fetch recommendations
if st.button("Get Recommendations"):
    try:
        data = fetch_recommendations(customer_id)
        
        if "error" in data:
            st.markdown(f'<p class="error">Error: {data["error"]}</p>', unsafe_allow_html=True)
        else:
            # Display recommendations
            st.header(f"Recommendations for Customer {data['customer_id']}")
            recommendations = data["recommendations"]
            chart_data = data["chart_data"]

            # Create a DataFrame for the table
            table_data = []
            for rec in recommendations:
                product_row = {
                    "Product Name": rec["product_name"],
                    "Score": round(rec["score"], 2),
                    "Premium ($/year)": chart_data["datasets"][1]["data"][chart_data["labels"].index(rec["product_name"])],
                    "Coverage ($100K)": chart_data["datasets"][2]["data"][chart_data["labels"].index(rec["product_name"])],
                    "Risk Level": chart_data["datasets"][3]["data"][chart_data["labels"].index(rec["product_name"])],
                    "Explanation": rec["explanation"]
                }
                table_data.append(product_row)
            df = pd.DataFrame(table_data)
            
            # Display table
            st.subheader("Recommendation Details")
            st.dataframe(df, use_container_width=True)

            # Bar chart
            st.subheader("Recommendation Metrics (Bar Chart)")
            bar_chart_html = f"""
            <canvas id="barChart" width="400" height="200"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
            <script>
                const ctx = document.getElementById('barChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'bar',
                    data: {json.dumps(chart_data)},
                    options: {{
                        scales: {{ y: {{ beginAtZero: true }} }},
                        plugins: {{ legend: {{ display: true }}, title: {{ display: true, text: 'Recommendation Metrics' }} }}
                    }}
                }});
            </script>
            """
            components.html(bar_chart_html, height=300)

            # Radar chart
            st.subheader("Product Comparison (Radar Chart)")
            radar_chart_data = {
                "labels": chart_data["labels"],
                "datasets": [
                    {
                        "label": dataset["label"],
                        "data": dataset["data"],
                        "backgroundColor": dataset["backgroundColor"].replace("0.5", "0.2"),
                        "borderColor": dataset["borderColor"],
                        "borderWidth": 1
                    } for dataset in chart_data["datasets"]
                ]
            }
            radar_chart_html = f"""
            <canvas id="radarChart" width="400" height="400"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
            <script>
                const ctxRadar = document.getElementById('radarChart').getContext('2d');
                new Chart(ctxRadar, {{
                    type: 'radar',
                    data: {json.dumps(radar_chart_data)},
                    options: {{
                        scales: {{ r: {{ beginAtZero: true, max: 1.0 }} }},
                        plugins: {{ legend: {{ display: true }}, title: {{ display: true, text: 'Product Comparison' }} }}
                    }}
                }});
            </script>
            """
            components.html(radar_chart_html, height=450)

            # Pie chart
            st.subheader("Recommendation Score Distribution (Pie Chart)")
            pie_chart_data = {
                "labels": chart_data["labels"],
                "datasets": [{
                    "label": "Recommendation Scores",
                    "data": chart_data["datasets"][0]["data"],
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.5)",
                        "rgba(54, 162, 235, 0.5)",
                        "rgba(255, 206, 86, 0.5)"
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)"
                    ],
                    "borderWidth": 1
                }]
            }
            pie_chart_html = f"""
            <canvas id="pieChart" width="400" height="400"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
            <script>
                const ctxPie = document.getElementById('pieChart').getContext('2d');
                new Chart(ctxPie, {{
                    type: 'pie',
                    data: {json.dumps(pie_chart_data)},
                    options: {{
                        plugins: {{ legend: {{ display: true }}, title: {{ display: true, text: 'Recommendation Score Distribution' }} }}
                    }}
                }});
            </script>
            """
            components.html(pie_chart_html, height=450)

    except requests.exceptions.RequestException as e:
        st.markdown(
            f'<p class="error">Error fetching recommendations: {str(e)}<br>'
            'Please ensure the Flask backend is running at http://127.0.0.1:5000 and no firewall is blocking the connection.</p>',
            unsafe_allow_html=True
        )
        logging.error(f"Failed to connect to Flask backend: {str(e)}")