import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Fraud Detection System", layout="wide")

# ---------------- LOAD MODEL ----------------
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("transactions.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.title("💳 Navigation")
menu = st.sidebar.radio("Go to", ["Fraud Detection", "Transaction Analytics", "About System"])

# =========================================================
# FRAUD DETECTION PAGE (PROFESSIONAL DESIGN)
# =========================================================
if menu == "Fraud Detection":

    st.title("💳 Smart Fraud Detection System")

    st.markdown("### Enter Transaction Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Client Name")
        amount = st.number_input("Transaction Amount")

        location = st.selectbox("Location", ["India", "USA", "UK", "Canada"])

    with col2:
        time_risk = st.selectbox("Time Risk (0=Morning, 3=Night)", [0,1,2,3])

        tx_type = st.selectbox("Transaction Type", ["ATM", "Card", "Online", "International"])

        frequency = st.number_input("Transaction Frequency")

    st.markdown("---")

    if st.button("🔍 Check Transaction"):

        foreign = 1 if location != "India" else 0
        high_amount = 1 if amount > 50000 else 0

        type_map = {"ATM":0, "Card":1, "Online":2, "International":3}
        tx_encoded = type_map[tx_type]

        features = [[
            amount,
            time_risk,
            tx_encoded,
            frequency,
            foreign,
            high_amount
        ]]

        prediction = model.predict(features)[0]

        st.markdown("### Result")

        if prediction == 1:
            st.error(f"🚨 FRAUD DETECTED for {name}")
        else:
            st.success(f"✅ NORMAL TRANSACTION for {name}")

# =========================================================
# TRANSACTION ANALYTICS (SMALL PROFESSIONAL DASHBOARD)
# =========================================================
elif menu == "Transaction Analytics":

    st.title("📊 Transaction Analytics Dashboard")

    total = len(df)
    fraud = len(df[df["Status"] == 1])
    normal = len(df[df["Status"] == 0])

    # ---------------- STATS CARDS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", total)
    col2.metric("Fraud Transactions", fraud)
    col3.metric("Normal Transactions", normal)

    st.markdown("---")

    # ---------------- SMALL PIE CHART ----------------
    fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))  # SMALL SIZE
    ax1.pie([normal, fraud],
            labels=["Normal", "Fraud"],
            autopct="%1.1f%%",
            startangle=90)
    ax1.set_title("Fraud Distribution", fontsize=10)

    st.pyplot(fig1, use_container_width=False)

    # ---------------- SMALL BAR CHART ----------------
    fig2, ax2 = plt.subplots(figsize=(4, 3))  # SMALL SIZE
    ax2.bar(["Normal", "Fraud"], [normal, fraud])
    ax2.set_title("Transaction Count", fontsize=10)

    st.pyplot(fig2, use_container_width=False)

# =========================================================
# ABOUT PAGE (ATTRACTIVE DESIGN)
# =========================================================
elif menu == "About System":

    st.title("ℹ About Fraud Detection System")

    st.markdown("""
    ### 🚀 Project Overview
    This system is a **Machine Learning-based Fraud Detection Web App** designed to identify suspicious financial transactions in real-time.

    ---

    ### 🧠 How It Works
    - Uses **Random Forest ML Model**
    - Analyzes transaction patterns:
        - Amount risk
        - Location risk
        - Time risk
        - Transaction type
        - Frequency behavior

    ---

    ### 📊 Features
    ✔ Real-time fraud detection  
    ✔ Clean dashboard UI  
    ✔ Analytics with charts  
    ✔ Professional banking-style interface  

    ---

    ### 🔐 Output Types
    - ✅ Normal Transaction  
    - 🚨 Fraud Transaction  

    ---

    ### 👨‍💻 Tech Stack
    - Python  
    - Streamlit  
    - Scikit-learn  
    - Pandas  
    - Matplotlib  

    ---

    ### 💡 Goal
    To simulate a **real-world banking fraud detection system** for educational and learning purposes.
    """)