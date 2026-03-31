# End-to-End Credit Card Fraud Detection System (Frontend)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://end-to-end-credit-card-fraud-detectiongit-bsdzhd84kzbzpbzrkb4p.streamlit.app/)

This repository contains the frontend component of a complete, end-to-end machine learning system for detecting credit card fraud. This user interface is built with Streamlit and serves as the interactive portal to a powerful XGBoost model hosted via a separate backend API.

**Live Application Link:** [https://end-to-end-credit-card-fraud-detectiongit-bsdzhd84kzbzpbzrkb4p.streamlit.app/](https://end-to-end-credit-card-fraud-detectiongit-bsdzhd84kzbzpbzrkb4p.streamlit.app/)

## Project Overview

The goal of this project is to provide a functional and intuitive tool for fraud detection. The system is architected with a decoupled frontend and backend, which is a modern standard for building scalable web applications. This Streamlit application handles all user interactions and communicates with a remote FastAPI backend to perform the actual machine learning inference.

## Features

The application provides two primary modes of operation:

1.  **Manual Entry:** A form-based interface for submitting the details of a single transaction. The app sends this data to the backend and displays the prediction (Normal or Fraudulent) in real-time.

2.  **Batch CSV Upload:** An efficient tool for analyzing large datasets. Users can upload a CSV file containing multiple transactions. The application sends the entire file to an optimized batch-processing endpoint on the backend, which returns predictions for all rows. This method is significantly faster than processing transactions one by one.

## System Architecture

This project demonstrates a classic client-server architecture.

*   **Frontend (This Repository):**
    *   **Framework:** Built with **Streamlit**, a Python library that enables rapid development of data-centric web applications.
    *   **Function:** Responsible for rendering the user interface, capturing user input, and communicating with the backend via HTTP requests.
    *   **Deployment:** Hosted on **Streamlit Community Cloud**, which integrates directly with this GitHub repository for continuous deployment.

*   **Backend (Separate Service):**
    *   **Framework:** A high-performance API built with **FastAPI**.
    *   **Function:** Hosts the trained XGBoost model and pre-processing scaler. It exposes secure endpoints that receive data from the frontend, perform inference, and return the prediction results.
    *   **Deployment:** The backend is containerized with Docker and deployed on **Hugging Face Spaces**.
    *   **Backend Link:** [https://huggingface.co/spaces/Amakxy/credit_card_fraud_detection_api](https://huggingface.co/spaces/Amakxy/credit_card_fraud_detection_api)

## Local Setup and Execution

To run this Streamlit application on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amakzy/End-to-End-Credit-Card-Fraud-Detection.git
    cd End-to-End-Credit-Card-Fraud-Detection
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the API connection:**
    The application needs to know the URL of the backend API. Create a file `.streamlit/secrets.toml` and add the following content to it:
    ```toml
    # .streamlit/secrets.toml
    API_URL = "https://amakxy-credit-card-fraud-detection-api.hf.space"
    ```

5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

The application will now be running and accessible in your web browser.
