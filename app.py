import streamlit as st
import requests
import pandas as pd

API_URL = "https://test-wgisin1x.b4a.run/predict"

st.set_page_config(page_title="Fraud Detection System", layout="wide")
st.title("Credit Card Fraud Detection Portal")
st.info(f"Currently targeting Backend API at: {API_URL}")
st.write("Real-time anomaly detection engine.")

tab1, tab2 = st.tabs(["Manual Entry", "Batch CSV Upload"])

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
                v_features[f"V{i}"] = st.number_input(f"V{i}", value=0.0)
                
        submit_btn = st.form_submit_button("Run Detection")
        
        if submit_btn:
            payload = {"Time": time_val, "Amount": amount_val, **v_features}
            try:
                response = requests.post(API_URL, json=payload, timeout=15)
                response.raise_for_status()
                result = response.json()
                
                if result['prediction'] == 1:
                    st.error(f"{result['message']} (Probability: {result['probability']:.4f})")
                else:
                    st.success(f"{result['message']} (Probability: {result['probability']:.4f})")
            except requests.exceptions.RequestException as e:
                st.error(f"API Connection Error: {e}")

with tab2:
    st.header("Batch CSV Prediction")
    uploaded_file = st.file_uploader("Upload creditcard.csv", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df_sample = df.head(50)
        st.write(f"Scanning first {len(df_sample)} transactions...")
        
        if st.button("Scan Database"):
            results =[]
            fraud_count = 0
            progress_bar = st.progress(0)
            
            # Using a Session to prevent network freezing on batch requests
            with requests.Session() as session:
                for idx, row in df_sample.iterrows():
                    payload = {"Time": row['Time'], "Amount": row['Amount']}
                    payload.update({f"V{i}": row[f"V{i}"] for i in range(1, 29)})
                    
                    try:
                        res = session.post(API_URL, json=payload, timeout=15).json()
                        is_fraud = res.get('prediction', 0) == 1
                    except requests.exceptions.RequestException:
                        is_fraud = False 
                    
                    if is_fraud:
                        fraud_count += 1
                    
                    results.append(is_fraud)
                    progress_bar.progress((idx + 1) / len(df_sample))
                
            df_sample['Is_Fraud'] = results
            st.write(f"Total Fraudulent Transactions Detected: {fraud_count}")
            
            def highlight_fraud(s):
                return['background-color: #ffcccc; color: black' if s.Is_Fraud else '' for _ in s]
            
            st.dataframe(df_sample.style.apply(highlight_fraud, axis=1))
