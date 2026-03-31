import streamlit as st
import requests
import pandas as pd

# URLs for API endpoints
SINGLE_PREDICT_URL = "https://amakxy-credit-card-fraud-detection-api.hf.space/predict"
BATCH_PREDICT_URL = "https://amakxy-credit-card-fraud-detection-api.hf.space/predict_batch"

st.set_page_config(page_title="Fraud Detection System", layout="wide")
st.title("Credit Card Fraud Detection Portal")
st.info(f"Connected to Backend API: {SINGLE_PREDICT_URL}")
st.write("Real-time anomaly detection engine.")

tab1, tab2 = st.tabs(["Manual Entry", "Batch CSV Upload"])

# --- TAB 1: Manual Entry ---
with tab1:
    st.header("Manual Transaction Entry")

    with st.form("manual_form"):
        col1, col2 = st.columns(2)
        with col1:
            time_val = st.number_input("Time (Seconds)", value=10000.0)
        with col2:
            amount_val = st.number_input("Amount ($)", value=250.0)

        st.write("PCA Features (V1 - V28)")
        v_features = {}
        cols = st.columns(4)
        for i in range(1, 29):
            with cols[(i - 1) % 4]:
                v_features[f"V{i}"] = st.number_input(f"V{i}", value=0.0, format="%.8f")

        submit_btn = st.form_submit_button("Run Detection")

        if submit_btn:
            payload = {"Time": time_val, "Amount": amount_val, **v_features}
            try:
                response = requests.post(SINGLE_PREDICT_URL, json=payload, timeout=15)
                response.raise_for_status()
                result = response.json()

                if result['prediction'] == 1:
                    st.error(f"{result['message']} (Probability: {result['probability']:.4f})")
                else:
                    st.success(f"{result['message']} (Probability: {result['probability']:.4f})")
            except requests.exceptions.RequestException as e:
                st.error(f"API Connection Error: {e}")

# --- TAB 2: Batch CSV Upload ---
with tab2:
    st.header("Batch CSV Prediction")
    uploaded_file = st.file_uploader("Upload creditcard.csv", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Preview of the first 5 rows of your uploaded data ({len(df)} total transactions):")
        st.dataframe(df.head())

        # The button now dynamically shows the total number of rows
        if st.button(f"Scan all {len(df)} transactions"):
            with st.spinner("Processing entire dataset... This may take a moment for large files."):
                try:
                    # Convert the FULL DataFrame to the list format for the API
                    transactions_list = df.to_dict(orient='records')
                    payload = {"transactions": transactions_list}

                    # Send the entire dataset in a single request.
                    # Increased timeout to handle very large datasets.
                    response = requests.post(BATCH_PREDICT_URL, json=payload, timeout=300)
                    response.raise_for_status()

                    results = response.json()
                    predictions = results['predictions']

                    # Add results to the original DataFrame
                    df['Is_Fraud_Prediction'] = predictions
                    fraud_count = df['Is_Fraud_Prediction'].sum()

                    st.success(f"Scan complete! Total Fraudulent Transactions Detected: {fraud_count}")

                    def highlight_fraud(s):
                        is_fraud = s.Is_Fraud_Prediction == 1
                        return ['background-color: #ffcccc; color: black' if is_fraud else '' for _ in s]

                    # Display the full DataFrame with highlighted results
                    st.dataframe(df.style.apply(highlight_fraud, axis=1))

                except requests.exceptions.Timeout:
                    st.error("API Error: The request timed out. The file may be too large for the current server configuration.")
                except requests.exceptions.RequestException as e:
                    st.error(f"API Connection Error: {e}")
                    st.error(f"Response from server: {e.response.text if e.response else 'No response'}")
