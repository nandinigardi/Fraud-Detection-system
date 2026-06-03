import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import time
import random
import csv
import requests

# =========================================================
# PAGE SETTINGS & PREMIUM THEME
# =========================================================

st.set_page_config(
    page_title="FraudGuard AI | Advanced Detection",
    page_icon="�️",
    layout="wide"
)

# CUSTOM CSS FOR PROFESSIONAL POLISHED FINTECH THEME
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Professional Soft Background */
    .stApp {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        color: #111827;
    }

    /* High-End Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Elegant Metric Cards with Accents */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 24px !important;
        border-radius: 12px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #4F46E5 !important; /* Indigo Accent */
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Specific Accent Colors for Metrics */
    div[data-testid="metric-container"]:nth-child(1) [data-testid="stMetric"] { border-top-color: #4F46E5 !important; } /* Blue */
    div[data-testid="metric-container"]:nth-child(2) [data-testid="stMetric"] { border-top-color: #EF4444 !important; } /* Red */
    div[data-testid="metric-container"]:nth-child(3) [data-testid="stMetric"] { border-top-color: #10B981 !important; } /* Green */

    /* Professional Buttons */
    div.stButton > button:first-child {
        background-color: #4F46E5;
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
    }
    div.stButton > button:hover {
        background-color: #4338CA;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
        transform: translateY(-1px);
    }
    
    /* Clean DataFrame/Table */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        background: white;
    }

    /* Status Badges (Capsule Style) */
    .status-capsule {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }

    /* Headings */
    h1 {
        color: #111827 !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 30px !important;
    }
    
    /* Input Styling */
    div[data-baseweb="input"], [data-baseweb="select"] {
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }

    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        [data-testid="stMetric"] {
            padding: 12px 16px !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
        h1 {
            font-size: 1.7rem !important;
            margin-bottom: 15px !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 14px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

model = pickle.load(
    open("fraud_model.pkl", "rb")
)

# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv("transactions.csv")

# REMOVE EXTRA SPACES FROM COLUMN NAMES
df.columns = df.columns.str.strip()

# =========================================================
# AUTHENTICATION SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# =========================================================
# LOGIN PAGE UI
# =========================================================

if not st.session_state.logged_in:
    # Center the login box
    _, auth_col, _ = st.columns([1, 1.5, 1])
    
    with auth_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); border: 1px solid rgba(255, 255, 255, 0.3);">
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="70">
                <h2 style="color: #0f172a; margin-top: 15px; font-weight: 800;">Fraud Detection System</h2>
                <p style="color: #64748b; font-size: 14px;">Enter credentials to access FraudGuard infrastructure</p>
            </div>
        """, unsafe_allow_html=True)
        # Clean professional form
        with st.form("login_form"):
            user = st.text_input("Administrator Username", placeholder="e.g. admin")
            pw = st.text_input("Security Key", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Login")
            
            if submit:
                if user == "admin" and pw == "bank789":
                    st.session_state.logged_in = True
                    st.success("Authorized. Loading encrypted environment...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Credentials")
    st.stop() 

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>🛡️ Secure Session</h3>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        logout()
    
    st.markdown("---")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60) 
    st.write(f"Identity: **Global Administrator**")
    
    st.markdown("---")
    menu = st.radio(
        "",
        ["🏠 Dashboard", "📡 Live Monitor", "🔍 Investigator", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.success("🟢 System Status: Online")

# =========================================================
# DASHBOARD (ANALYTICS & RECORDS)
# =========================================================

if menu == "🏠 Dashboard":
    st.title("🏠 System Dashboard")
    
    # RELOAD DATA REFRESHING
    df = pd.read_csv("transactions.csv")
    df.columns = df.columns.str.strip()
    
    tab1, tab2 = st.tabs(["📊 Performance Analytics", "📋 Transaction Logs"])

    with tab1:
        st.markdown("### System-Wide Analytics")
        # RELOAD DATA REFRESHING
        df = pd.read_csv("transactions.csv")
        
        # METRICS
        total_count = len(df)
        fraud_count = len(df[df["Status"] == 1])
        # Status 2: Manual Override, Status 3: Manual Investigator Entry
        manual_count = len(df[df["Status"].isin([2, 3])])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", total_count)
        col2.metric("Fraud Detected", fraud_count, delta="ALERTS", delta_color="inverse")
        col3.metric("Manually Approved", manual_count, delta="HUMAN OVERRIDE", delta_color="off")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            fig1, ax1 = plt.subplots(figsize=(4,4))
            ax1.pie([len(df[df["Status"] == 0]) + manual_count, fraud_count], labels=["Safe", "Fraud"], autopct="%1.1f%%", startangle=90, colors=["#10B981", "#EF4444"])
            ax1.set_title("Safety Distribution")
            st.pyplot(fig1)
        with c2:
            fig2, ax2 = plt.subplots(figsize=(4.5,4))
            ax2.bar(["Normal", "Fraud", "Manual"], [len(df[df["Status"] == 0]), fraud_count, manual_count], color=["#10B981", "#EF4444", "#F59E0B"])
            ax2.set_title("Case Categorization")
            st.pyplot(fig2)

        st.markdown("---")
        # SMALLER REGIONAL CHART
        sc1, sc2 = st.columns([1, 1])
        with sc1:
            st.markdown("### Geographic Distribution")
            location_counts = df['Location'].value_counts()
            st.bar_chart(location_counts, color="#4F46E5")
        with sc2:
            st.write("") # Empty space for balance

    with tab2:
        st.markdown("### Transaction Database")
        
        # SEARCH AND FILTER ROW
        f_col1, f_col2 = st.columns([2, 1])
        with f_col1:
            search = st.text_input("🔍 Search Client Name", placeholder="Enter name...")
        with f_col2:
            status_filter = st.selectbox("Filter by Category", ["All Records", "Normal (Safe)", "Fraud (Blocked)", "Manual Approvals"])
        
        display_df = df.copy()
        
        # APPLY SEARCH
        if search:
            display_df = display_df[display_df["Name"].str.contains(search, case=False, na=False)]
        
        # APPLY STATUS FILTER
        if status_filter == "Normal (Safe)":
            display_df = display_df[display_df["Status"] == 0]
        elif status_filter == "Fraud (Blocked)":
            display_df = display_df[display_df["Status"] == 1]
        elif status_filter == "Manual Approvals":
            display_df = display_df[display_df["Status"].isin([2, 3])]
        
        # ADD LABELS
        display_df['Status_Label'] = display_df['Status'].astype(str).map({
            "0": "NORMAL",
            "1": "FRAUD",
            "2": "MANUAL OVERRIDE",
            "3": "MANUAL ENTRY"
        })

        def style_rows(val):
            if val == "FRAUD": return 'background-color: #FEE2E2; color: #991B1B'
            if val == "MANUAL OVERRIDE": return 'background-color: #FEF3C7; color: #92400E'
            if val == "MANUAL ENTRY": return 'background-color: #E0F2FE; color: #075985'
            return 'background-color: #D1FAE5; color: #065F46'

        st.dataframe(
            display_df.style.map(style_rows, subset=['Status_Label']),
            use_container_width=True
        )

# =========================================================
# LIVE MONITOR
# =========================================================

elif menu == "📡 Live Monitor":
    # (The simulation logic stays here, but refined)
    st.title("📡 Live Surveillance Feed")
    
    if "sim_running" not in st.session_state:
        st.session_state.sim_running = False

    if not st.session_state.sim_running:
        if st.button("🚀 Start Surveillance Session"):
            st.session_state.sim_running = True
            st.rerun()
    else:
        if st.button("🛑 Terminate Session"):
            st.session_state.sim_running = False
            st.rerun()

    if st.session_state.sim_running:
        # SECURE CUSTOMER DATABASE
        user_profiles = {
            "Amit Sharma": {"phone": "+91 98765-10293", "email": "amit.s@bank.com", "tier": "Gold"},
            "Priya Patel": {"phone": "+91 88293-11022", "email": "priya.p@bank.com", "tier": "Platinum"},
            "John Smith": {"phone": "+1 415-555-0199", "email": "j.smith@corp.com", "tier": "Silver"},
            "Sara Khan": {"phone": "+91 77334-99810", "email": "sara.k@fastmail.com", "tier": "Gold"},
            "Vikram Singh": {"phone": "+91 99001-22345", "email": "v.singh@indiamail.in", "tier": "Diamond"},
            "Elena Rossi": {"phone": "+39 02-1234567", "email": "e.rossi@eurobank.it", "tier": "Platinum"},
            "Li Wei": {"phone": "+86 10-65432100", "email": "li.wei@chinabank.cn", "tier": "Gold"},
            "David Cohen": {"phone": "+972 3-1234567", "email": "d.cohen@isramail.il", "tier": "Silver"}
        }
        
        # Initialize session state for coordination
        if "active_tx" not in st.session_state:
            name_s = random.choice(list(user_profiles.keys()))
            amt_s = random.randint(500, 180000)
            loc_s = random.choice(["India", "USA", "UK", "Canada", "Germany", "Japan"])
            time_s = random.choice(["Morning", "Afternoon", "Evening", "Night"])
            type_s = random.choice(["ATM", "Card", "Online", "International"])
            freq_s = random.randint(1, 20)
            
            # Feature Engineering for Prediction
            time_map = {"Morning": 0, "Afternoon": 1, "Evening": 2, "Night": 3}
            type_map = {"ATM": 0, "Card": 1, "Online": 2, "International": 3}
            foreign = 1 if loc_s != "India" else 0
            high_amt = 1 if amt_s > 50000 else 0
            t_enc = time_map[time_s]
            tx_enc = type_map[type_s]
            
            # Predict
            pred = model.predict([[amt_s, t_enc, tx_enc, freq_s, foreign, high_amt]])[0]
            risk = random.randint(75, 99) if pred == 1 else random.randint(5, 45)
            
            # LOCK ALL DATA INTO MEMORY
            st.session_state.active_tx = {
                "name": name_s, "amt": amt_s, "loc": loc_s, "time": time_s, "type": type_s,
                "freq": freq_s, "risk": risk, "pred": pred, "t_enc": t_enc, "tx_enc": tx_enc
            }

        tx = st.session_state.active_tx
        
        # DISPLAY LOCKED TRANSACTION
        st.info(f"Incoming: **{tx['name']}** | Amount: **₹{tx['amt']:,.2f}**")
        
        if tx['risk'] > 70:
            st.warning(f"🚨 ALERT: High Risk Profile ({tx['risk']}%)")
            
            # IDENTITY PROFILE
            with st.expander("🔍 View Identity Profile"):
                profile = user_profiles.get(tx['name'])
                p_col1, p_col2 = st.columns([1, 2])
                with p_col1:
                    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80) 
                with p_col2:
                    st.write(f"**Phone:** {profile['phone']}")
                    st.write(f"**Email:** {profile['email']}")
            
            # SYSTEM TIMER (Stable single-pulse logic)
            if "timer_start" not in st.session_state:
                st.session_state.timer_start = 60
                
            timer_p = st.empty()
            btn_p = st.empty()
            
            # Function to save decision
            def save_decision(status_code):
                with open("transactions.csv", "a", newline='') as f:
                    csv.writer(f).writerow([tx['name'], tx['amt'], tx['loc'], tx['t_enc'], tx['type'], tx['freq'], status_code])
                del st.session_state.active_tx
                if "timer_start" in st.session_state: del st.session_state.timer_start
                st.rerun()

            # SHOW BUTTONS FIRST (So they are clickable)
            with btn_p.container():
                c1, c2 = st.columns(2)
                if c1.button("✅ Authorize"): save_decision(2)
                if c2.button("🚨 Block"): save_decision(1)

            # TIMER DECREMENT
            s = st.session_state.timer_start
            timer_p.markdown(f"<p style='color: #ef4444; font-size: 14px; font-weight: 700; text-align: right; margin-bottom: 0px;'>DECISION TIMEOUT: {s}s</p>", unsafe_allow_html=True)
            
            if s > 0:
                time.sleep(1)
                st.session_state.timer_start -= 1
                st.rerun()
            else:
                st.error("🛑 TIMEOUT: Transaction Auto-Blocked.")
                time.sleep(1)
                save_decision(1)
        else:
            st.success(f"✅ Secure Case (Risk: {tx['risk']}%)")
            with open("transactions.csv", "a", newline='') as f:
                csv.writer(f).writerow([tx['name'], tx['amt'], tx['loc'], tx['t_enc'], tx['type'], tx['freq'], 0])
            time.sleep(2)
            del st.session_state.active_tx
            st.rerun()
        st.session_state.sim_running = False

# =========================================================
# INVESTIGATOR (MANUAL)
# =========================================================

elif menu == "🔍 Investigator":
    st.title("🔍 Fraud Investigator")
    st.markdown("### Manual Entry & Intelligence Check")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            name_in = st.text_input("Name")
            amt_in = st.number_input("Amount", min_value=0)
        with c2:
            loc_in = st.selectbox("Location", ["India", "USA", "UK", "Canada"])
            time_in = st.selectbox("Time", ["Morning", "Afternoon", "Evening", "Night"])
        
        type_in = st.selectbox("Type", ["ATM", "Card", "Online", "International"])

        if st.button("🕵️ Start Investigation"):
            # FREQUENCY CALC
            count = len(df[df['Name'].str.lower() == name_in.strip().lower()])
            calc_freq = count + 1
            
            st.write(f"History Check: Found **{count}** records. (Total: {calc_freq})")
            
            time_map = {"Morning": 0, "Afternoon": 1, "Evening": 2, "Night": 3}
            type_map = {"ATM": 0, "Card": 1, "Online": 2, "International": 3}
            
            pred_in = model.predict([[amt_in, time_map[time_in], type_map[type_in], calc_freq, 1 if loc_in != "India" else 0, 1 if amt_in > 50000 else 0]])[0]
            
            if pred_in == 1: st.error("🚨 FRAUD DETECTED")
            else: st.success("✅ SECURE TRANSACTION")
            
            with open("transactions.csv", "a", newline='') as f:
                # We save with Status 3 so it shows up in "Manual" filter
                csv.writer(f).writerow([name_in, amt_in, loc_in, time_map[time_in], type_in, calc_freq, 3])

# =========================================================
# SETTINGS
# =========================================================

elif menu == "⚙️ Settings":
    st.title("⚙️ System Management")
    
    with st.expander("About This Project"):
        st.markdown("""
        ## Project Overview
        FraudGuard AI is a sophisticated Machine Learning platform built to detect and prevent banking fraud. It uses advanced algorithms to analyze transaction patterns in real-time, providing security administrators with an intelligence-driven dashboard for active risk management.

        ---

        ## Key Features
        1. Real-Time Surveillance: Monitors live transaction traffic and identifies high-risk activities instantly.
        2. AI Risk Scoring: Evaluates every transaction using a Random Forest model to determine its safety.
        3. Admin Control Portal: A secure, authenticated environment for managing banking records and user profiles.
        4. Intelligence History: Automatically calculates transaction frequency by analyzing historical patterns.
        5. Data Integrity Tools: Comprehensive utilities for exporting databases and repairing historical data sets.
        """)

    with st.expander("Data Management"):
        st.write("Export your database to CSV format for backup or analysis.")
        csv_exp = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Transaction Database",
            data=csv_exp,
            file_name="fraudGuard_records.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.write("🛰️ **Advanced Database Repair**")
        st.info("Use this if your historical frequency numbers look random or incorrect.")
        if st.button("🔄 Sync & Fix Historical Frequency"):
            # SAFETY: Create backup
            df.to_csv("transactions_v2_backup.csv", index=False)
            
            # FIX LOGIC: Group by name and count occurrences in order
            df['Name'] = df['Name'].fillna("Unknown")
            df['Frequency'] = df.groupby('Name').cumcount() + 1
            
            # SAVE BACK
            df.to_csv("transactions.csv", index=False)
            st.success("✅ Database Repaired! All historical frequencies have been recalculated.")
            st.rerun()