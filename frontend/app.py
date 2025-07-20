# main.py

import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
from PIL import Image
import csv
# ---------------------------- Configuration ----------------------------
st.set_page_config(page_title="AI Hiring Predictor", layout="wide")
banner = Image.open("assets/banner.png")
st.image(banner, use_container_width=True)
st.caption("🔍 Powered by AI | Smart Hiring Decisions Made Easy")

# Theme selection
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

theme_choice = st.sidebar.radio("🎨 Theme", ["Light 🌞", "Dark 🌙"], 
                                index=0 if st.session_state.theme == "Light" else 1)

st.session_state.theme = "Light" if "Light" in theme_choice else "Dark"

# Apply visual theme
if st.session_state.theme == "Dark":
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #0e1117 !important;
            color: #f0f0f0 !important;
        }
        .stTextInput > div > div > input {
            background-color: #262730;
            color: white;
        }
        .stSelectbox > div > div {
            background-color: #262730;
            color: white;
        }
        .stRadio > div {
            color: white;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)


# ---------------------------- Session Init ----------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------------------- Auto-create users.csv ----------------------------
if not os.path.exists("users.csv"):
    with open("users.csv", mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])
        writer.writerow(["admin", "admin123"])

# ---------------------------- Functions ----------------------------
def check_credentials(username, password):
    df = pd.read_csv("users.csv")
    return ((df["username"] == username) & (df["password"] == password)).any()

def add_new_user(username, password):
    df = pd.read_csv("users.csv")
    if username in df["username"].values:
        return False
    with open("users.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, password])
    return True

# ---------------------------- Load Model ----------------------------
model_path = 'C:/Users/ASUS/Desktop/predictive-hiring-app/backend/model/predictive_model.pkl'
model = pickle.load(open(model_path, 'rb'))

# Mappings
job_role_map = {"Software Engineer": 340, "Data Analyst": 350, "ML Engineer": 360}
industry_map = {"Information Technology": 938, "Finance": 940, "Healthcare": 950}
current_title_map = {"Intern": 394, "Junior Developer": 400, "Senior Analyst": 410}
location_map = {"Chennai": 110, "Bangalore": 115, "Mumbai": 120}

# Reverse mappings
job_role_map_rev = {v: k for k, v in job_role_map.items()}
industry_map_rev = {v: k for k, v in industry_map.items()}
current_title_map_rev = {v: k for k, v in current_title_map.items()}
location_map_rev = {v: k for k, v in location_map.items()}

# ---------------------------- Navigation ----------------------------
menu = st.sidebar.radio("🌐 Navigate", ["🏠 Home", "💼 Hiring Predictor", "🔐 Admin Dashboard"])

# ---------------------------- HOME ----------------------------
if menu == "🏠 Home":

    if st.session_state["page"] == "home":
        st.markdown("""
        <style>
        .home-container {
            padding: 3rem;
            background-color: #f5f9ff;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            margin-top: 3rem;
        }
        .home-title {
            text-align: center;
            font-size: 40px;
            color: #2E86C1;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .home-subtitle {
            text-align: center;
            font-size: 20px;
            color: #555;
            margin-bottom: 30px;
        }
        .home-highlight {
            background-color: #D4EDDA;
            padding: 1rem;
            border-left: 6px solid #28A745;
            font-size: 16px;
            color: #155724;
            margin-bottom: 2rem;
            border-radius: 6px;
        }
        </style>
        <div class="home-container">
            <div class="home-title">🤖 AI Hiring Predictor</div>
            <div class="home-subtitle">Smarter Talent Decisions Powered by Machine Learning</div>
            <div class="home-highlight">
                💡 Predict hiring potential of candidates<br>
                📊 Visualize analytics in the admin dashboard<br>
                🔐 Secure login for both users and admins
            </div>
    """, unsafe_allow_html=True)
    st.info("➡️ Use the sidebar to access the prediction form or admin dashboard.")

# ---------------------------- USER LOGIN ----------------------------
if menu == "💼 Hiring Predictor" and not st.session_state.logged_in:
    st.session_state.page = "login"
    st.markdown("""
        <div class="login-container">
            <div class="login-title">🔐 Welcome to AI Hiring Predictor</div>
            <div class="login-sub">Please login or sign up to continue</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_type = st.radio("👥 Select Action", ["Login", "Signup"], horizontal=True)
        user_name = st.text_input("🧑 Username")
        user_pass = st.text_input("🔒 Password", type="password")

        if login_type == "Login":
            if st.button("🔓 Login", use_container_width=True):
                if check_credentials(user_name, user_pass):
                    st.session_state.logged_in = True
                    st.session_state.user = user_name
                    st.session_state.page = "predictor"
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")
        else:
            if st.button("➕ Sign Up", use_container_width=True):
                if add_new_user(user_name, user_pass):
                    st.success("✅ Account created! You can now log in.")
                else:
                    st.warning("⚠️ Username already exists.")

# ---------------------------- HIRING PREDICTOR ----------------------------
if st.session_state.page == "predictor":
    
    if "prediction_done" not in st.session_state:
        st.session_state.prediction_done = False

    st.sidebar.markdown(f"👋 Logged in as: `{st.session_state.user}`")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "home"
        st.session_state.prediction_done = False
        st.rerun()

    if not st.session_state.prediction_done:
        st.markdown("<h1 style='color:#4CAF50;'>💼 AI Hiring & Talent Predictor</h1>", unsafe_allow_html=True)
        with st.expander("ℹ️ About this App"):
            st.write("""
                This AI-powered tool predicts the hiring possibility of a candidate based on their profile. 
                It helps HRs or students assess what factors influence hiring decisions.
            """)

        st.markdown("## 📝 Candidate Profile Form")
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.slider("🎂 Age", 18, 60, 25)
                gender = st.radio("👤 Gender", ["Male", "Female"])
                education = st.selectbox("🎓 Education Level", ["UG", "PG", "PhD"])
                experience = st.slider("💼 Years of Experience", 0, 30, 2)
            with col2:
                location_label = st.selectbox("📍 Preferred Location", list(location_map.keys()))
                income_level = st.selectbox("💰 Current Income Level", ["Low", "Medium", "High"])
                hike = st.slider("📈 Expected Salary Hike (%)", 0, 100, 10)

            col3, col4 = st.columns(2)
            with col3:
                job_role_label = st.selectbox("💼 Target Job Role", list(job_role_map.keys()))
                current_title_label = st.selectbox("👔 Current Job Title", list(current_title_map.keys()))
            with col4:
                industry_label = st.selectbox("🏢 Industry Sector", list(industry_map.keys()))
                upskilled = st.radio("🤖 AI Upskilled?", ["Yes", "No"])
                upskill_type = st.selectbox("📚 AI Upskilling Type", ["Online", "Offline", "None"])

            submitted = st.form_submit_button("🚀 Predict Hiring Possibility")

        if submitted:
            # Store values for reuse on result page
            st.session_state.inputs = {
                "age": age, "gender": gender, "education": education, "experience": experience,
                "location_label": location_label, "income_level": income_level, "hike": hike,
                "job_role_label": job_role_label, "current_title_label": current_title_label,
                "industry_label": industry_label, "upskilled": upskilled, "upskill_type": upskill_type
            }
            st.session_state.prediction_done = True
            st.rerun()

    else:
        # Get previous input
        inputs = st.session_state.inputs
        st.markdown("<h2 style='color:#2E86C1;'>📊 Prediction Results</h2>", unsafe_allow_html=True)

        gender_val = 1 if inputs["gender"] == "Male" else 0
        edu_val = {"UG": 0, "PG": 1, "PhD": 2}[inputs["education"]]
        income_val = {"Low": 0, "Medium": 1, "High": 2}[inputs["income_level"]]
        upskill_val = 1 if inputs["upskilled"] == "Yes" else 0
        upskill_type_val = {"Online": 0, "Offline": 1, "None": 2}[inputs["upskill_type"]]
        job_role = job_role_map[inputs["job_role_label"]]
        industry = industry_map[inputs["industry_label"]]
        current_title = current_title_map[inputs["current_title_label"]]
        location = location_map[inputs["location_label"]]

        input_data = pd.DataFrame([[
            inputs["age"], gender_val, edu_val, inputs["experience"], job_role,
            industry, current_title, income_val, location,
            upskill_val, upskill_type_val, inputs["hike"]
        ]], columns=[
            'Age', 'Gender', 'Education Level', 'Years of Experience',
            'Job Role', 'Industry', 'Current Job Title', 'Income Level',
            'Location', 'AI Upskilling', 'AI Upskilling Type',
            'Percentage Hike in Salary'
        ])

        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][prediction]

        st.success(f"🎯 Prediction: {'Likely to be Selected ✅' if prediction else 'Not Likely ❌'} (Confidence: {prob:.2f})")

        st.markdown("### 💡 Suggestions to Improve Profile")
        if inputs["upskilled"] == "No":
            st.info("📘 Consider enrolling in an AI/ML course to improve hiring chances.")
        if inputs["experience"] < 1:
            st.warning("🛠️ Gain hands-on experience through internships or real projects.")
        if inputs["income_level"] == "High" and inputs["hike"] > 50:
            st.warning("💸 High income and high hike expected. Consider realistic benchmarks.")
        if inputs["education"] == "UG" and inputs["upskill_type"] == "None":
            st.info("🎓 Consider pursuing PG or upskilling programs for better prospects.")
        if inputs["current_title_label"] == "Intern":
            st.info("👔 Try transitioning to junior/full-time roles to increase selection chances.")

        if hasattr(model, "feature_importances_"):
            st.markdown("### 📊 Feature Importance")
            fig, ax = plt.subplots()
            ax.barh(input_data.columns, model.feature_importances_, color="skyblue")
            ax.set_title("Top Features for Hiring Decision")
            st.pyplot(fig)

        st.markdown("### 📝 Prediction Summary")
        st.success(f"""
- 🧑 Role Applied: **{inputs["job_role_label"]}**
- 📍 Location: **{inputs["location_label"]}**
- 💼 Experience: **{inputs["experience"]} years**
- 🧠 Upskilled: **{inputs["upskilled"]}**
- 🎯 Result: **{'Selected' if prediction == 1 else 'Not Selected'}** (Confidence: {prob:.2f})
        """)

        # Save to history
        input_data['Prediction'] = prediction
        input_data.to_csv("history.csv", mode='a', index=False, header=not os.path.exists("history.csv"))

        # Button to go back to form
        if st.button("🔙 Back to Form"):
            st.session_state.prediction_done = False
            st.rerun()

# ---------------------------- ADMIN DASHBOARD ----------------------------
if menu == "🔐 Admin Dashboard" and not st.session_state.admin_logged_in:
    st.markdown("## 🔐 Admin Login", unsafe_allow_html=True)
    with st.container():
        admin_user = st.text_input("👤 Admin Username")
        admin_pass = st.text_input("🔒 Password", type="password")
        if st.button("Admin Login"):
            if admin_user == "admin" and admin_pass == "admin123":
                st.session_state.admin_logged_in = True
                st.session_state.page = "admin"
                st.rerun()
            else:
                st.error("❌ Invalid admin credentials.")

if st.session_state.page == "admin":
    st.markdown("<h1 style='color:#6C3483;'>📊 Admin Dashboard</h1>", unsafe_allow_html=True)

    st.sidebar.markdown("👑 Logged in as: Admin")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.admin_logged_in = False
        st.session_state.page = "home"
        st.rerun()

    if not os.path.exists("history.csv"):
        st.warning("No prediction history found.")
    else:
        df = pd.read_csv("history.csv")
        df['Job Role'] = df['Job Role'].map(job_role_map_rev)
        df['Industry'] = df['Industry'].map(industry_map_rev)
        df['Current Job Title'] = df['Current Job Title'].map(current_title_map_rev)
        df['Location'] = df['Location'].map(location_map_rev)
        df['AI Upskilling'] = df['AI Upskilling'].map({1: 'Yes', 0: 'No'})
        df['Prediction'] = df['Prediction'].map({1: 'Selected', 0: 'Not Selected'})
        df['Gender'] = df['Gender'].map({1: 'Male', 0: 'Female'})
        df['Education Level'] = df['Education Level'].map({0: 'UG', 1: 'PG', 2: 'PhD'})
        df['Income Level'] = df['Income Level'].map({0: 'Low', 1: 'Medium', 2: 'High'})
        df['AI Upskilling Type'] = df['AI Upskilling Type'].map({0: 'Online', 1: 'Offline', 2: 'None'})

        # KPI Metrics
        total = len(df)
        selected = df['Prediction'].value_counts().get('Selected', 0)
        not_selected = df['Prediction'].value_counts().get('Not Selected', 0)

        st.markdown("### 📈 Overview Metrics")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Predictions", total)
        kpi2.metric("Selected", selected)
        kpi3.metric("Not Selected", not_selected)

        st.markdown("### 🔎 Prediction Summary Table")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📊 Insights")
        col1, col2 = st.columns(2)
        with col1:
            fig1, ax1 = plt.subplots()
            df['Prediction'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=["#2ECC71", "#E74C3C"], ax=ax1)
            ax1.set_ylabel('')
            ax1.set_title("Selection Rate")
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots()
            df['Job Role'].value_counts().plot(kind='bar', color='#3498DB', ax=ax2)
            ax2.set_title("Popular Job Roles")
            st.pyplot(fig2)

        st.markdown("### 🔍 Filter Prediction History")
        col1, col2 = st.columns(2)
        with col1:
            role = st.selectbox("Filter by Job Role", ["All"] + sorted(df['Job Role'].unique()))
        with col2:
            loc = st.selectbox("Filter by Location", ["All"] + sorted(df['Location'].unique()))

        filtered_df = df.copy()
        if role != "All":
            filtered_df = filtered_df[filtered_df['Job Role'] == role]
        if loc != "All":
            filtered_df = filtered_df[filtered_df['Location'] == loc]

        st.markdown(f"📌 Showing **{len(filtered_df)}** result(s) after filter")
        st.dataframe(filtered_df, use_container_width=True)

# ---------------------------- Footer ----------------------------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("🔒 *All data processed locally.*")
with col2:
    st.markdown("📧 [Contact Developer](mailto:2309poojamurugan@gmail.com)") 