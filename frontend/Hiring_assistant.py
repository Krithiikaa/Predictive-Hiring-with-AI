import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
from PIL import Image
import csv
from supabase import create_client, Client
from dotenv import load_dotenv
import os

import streamlit as st
from supabase import create_client, Client

# Supabase via Streamlit Secrets
url: str = st.secrets["supabase"]["url"]
key: str = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# ---------------------------- Setup ----------------------------
st.set_page_config(page_title="AI Hiring Predictor", layout="wide")
import os
from PIL import Image

# Compute the path to this file's directory
HERE = os.path.dirname(__file__)

# Build a cross‑platform path to your assets folder
banner_path = os.path.join(HERE, "assets", "banner.png")
banner = Image.open(banner_path)

st.image(banner, use_container_width=True)

# ---------------------------- Initialize Session ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------------------- Auto Create Users File ----------------------------
if not os.path.exists("users.csv"):
    with open("users.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])
        writer.writerow(["admin", "admin123"])

# ---------------------------- Functions ----------------------------
def check_credentials(username, password):
    response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
    return len(response.data) > 0

def add_new_user(username, password):
    existing_user = supabase.table("users").select("*").eq("username", username).execute()
    if existing_user.data:
        return False
    supabase.table("users").insert({"username": username, "password": password}).execute()
    return True


# ---------------------------- Mappings ----------------------------
job_role_map = {"Software Engineer": 340, "Data Analyst": 350, "ML Engineer": 360}
industry_map = {"Information Technology": 938, "Finance": 940, "Healthcare": 950}
current_title_map = {"Intern": 394, "Junior Developer": 400, "Senior Analyst": 410}
location_map = {"Chennai": 110, "Bangalore": 115, "Mumbai": 120}

job_role_map_rev = {v: k for k, v in job_role_map.items()}
industry_map_rev = {v: k for k, v in industry_map.items()}
current_title_map_rev = {v: k for k, v in current_title_map.items()}
location_map_rev = {v: k for k, v in location_map.items()}

# ---------------------------- Load Model ----------------------------
import os
import pickle

# Compute path to THIS script’s directory
HERE = os.path.dirname(__file__)

# Build a path to …/backend/model/predictive_model.pkl
model_path = os.path.normpath(
    os.path.join(HERE, "..", "backend", "model", "predictive_model.pkl")
)

# Load the model
with open(model_path, "rb") as f:
    model = pickle.load(f)

model = pickle.load(open(model_path, 'rb'))

# ---------------------------- Home Page ----------------------------
if st.session_state.page == "home":
    st.markdown("""
        <style>
            .stApp {
                background-image: url('https://images.unsplash.com/photo-1581093588401-75bfa3d9f71b?auto=format&fit=crop&w=1650&q=80');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            .home-title {
                font-size: 40px;
                font-weight: 700;
                color: #ffffff;
                text-align: center;
                margin-top: 2rem;
                text-shadow: 1px 1px 3px #000;
            }
            .home-subtitle {
                font-size: 18px;
                color: #f1f1f1;
                text-align: center;
                margin-bottom: 2rem;
                text-shadow: 1px 1px 2px #000;
            }
            .login-box {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 16px;
                padding: 2rem 2.5rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
                margin-top: 2rem;
            }
            .stTextInput input {
                background-color: #f0f4f8 !important;
                border-radius: 8px !important;
            }
            .stButton>button {
                background-color: #2980B9;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 0.5rem 1rem;
            }
            .stButton>button:hover {
                background-color: #21618C;
            }
            .stRadio > div {
                justify-content: center;
            }
        </style>
        <div class='home-title'>🌟 Welcome to AI Hiring Predictor</div>
        <div class='home-subtitle'>Smart hiring insights powered by AI — Login as Admin or User to begin</div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        
        role = st.radio("Select Role", ["Admin", "User"], horizontal=True)
        user = st.text_input("👤 Username")
        passwd = st.text_input("🔒 Password", type="password")

        if role == "Admin":
            if st.button("Login as Admin", use_container_width=True):
                if user == "admin" and passwd == "admin123":
                    st.session_state.admin_logged_in = True
                    st.session_state.page = "admin"
                    st.success("✅ Logged in as Admin")
                    st.rerun()
                else:
                    st.error("❌ Invalid admin credentials.")
        else:
            auth_type = st.radio("Choose", ["Login", "Signup"], horizontal=True)
            if auth_type == "Login":
                if st.button("🔓 User Login", use_container_width=True):
                    if check_credentials(user, passwd):
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.page = "predictor"
                        st.success(f"✅ Welcome, {user}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid user credentials.")
            else:
                if st.button("➕ Sign Up", use_container_width=True):
                    if len(user.strip()) < 3:
                        st.warning("⚠️ Username must be at least 3 characters.")
                    elif len(passwd) < 6:
                        st.warning("⚠️ Password must be at least 6 characters.")
                    elif add_new_user(user.strip(), passwd):
                        st.success("✅ Account created! You can now log in.")
                    else:
                        st.warning("⚠️ Username already exists.")
        
        st.markdown("</div>", unsafe_allow_html=True)



# ---------------------------- Admin Dashboard ----------------------------
if st.session_state.page == "admin":
    st.markdown("""
        <style>
            .dashboard-title {
                font-size: 36px;
                font-weight: bold;
                color: #2E86C1;
                margin-bottom: 1rem;
            }
            .section-title {
                font-size: 22px;
                font-weight: 600;
                color: #154360;
                margin-top: 2rem;
            }
            .metric-card {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                text-align: center;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.success("👑 Admin Mode")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "home"
        st.session_state.admin_logged_in = False
        st.rerun()

    st.markdown("<div class='dashboard-title'>📊 Admin Dashboard</div>", unsafe_allow_html=True)

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

        total = len(df)
        selected = df['Prediction'].value_counts().get('Selected', 0)
        not_selected = df['Prediction'].value_counts().get('Not Selected', 0)

        st.markdown("<div class='section-title'>📈 Overview Metrics</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Total Predictions", total)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Selected", selected)
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Not Selected", not_selected)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🔎 Prediction Summary Table</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        st.markdown("<div class='section-title'>📊 Insights</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig1, ax1 = plt.subplots()
            df['Prediction'].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'red'], ax=ax1)
            ax1.set_ylabel('')
            ax1.set_title("Hiring Outcome")
            st.pyplot(fig1)
        with col2:
            fig2, ax2 = plt.subplots()
            df['Job Role'].value_counts().plot(kind='bar', color='skyblue', ax=ax2)
            ax2.set_title("Popular Roles")
            st.pyplot(fig2)

        st.markdown("<div class='section-title'>🔍 Filter Prediction History</div>", unsafe_allow_html=True)
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

# ---------------------------- Hiring Predictor ----------------------------
if st.session_state.page == "predictor":
    if "prediction_done" not in st.session_state:
        st.session_state.prediction_done = False
    st.sidebar.markdown(f"👋 Logged in as: `{st.session_state.user}`")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "home"
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
    
    if not st.session_state.prediction_done:
        st.markdown("""
        <style>
        .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #2C3E50;
        margin-top: 10px;
        padding: 10px 0;
        border-bottom: 3px solid #4CAF50;
        text-align: center;
        }
        .expander .streamlit-expanderHeader {
        font-size: 20px;
        font-weight: 600;
        color: #1E8449;
        }
        </style>
        <div class='main-title'>💼 AI Hiring & Talent Predictor</div>
        """, unsafe_allow_html=True)

        with st.expander("ℹ️ About this App"):
            st.markdown("""
    <div style='font-size: 16px; color: #555; line-height: 1.6;'>
        This <strong>AI-powered hiring assistant</strong> helps HR professionals and job seekers assess the likelihood of candidate selection based on profile details.<br><br>
        Built with machine learning, it delivers real-time predictions and personalized improvement suggestions.
    </div>
    """, unsafe_allow_html=True)
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

        result_text = "✅ Likely to be Selected" if prediction else "❌ Not Likely to be Selected"
        result_color = "#28a745" if prediction else "#c0392b"

        st.markdown(f"""
        <div style="background-color:#f9f9f9; padding: 20px; border-left: 6px solid {result_color}; border-radius: 10px;">
        <h3 style="color:{result_color};">🎯 Prediction Result</h3>
        <p style="font-size:18px;">{result_text}</p>
        <p><b>Confidence Score:</b> {prob:.2f}</p>
        </div>
        """, unsafe_allow_html=True)


        st.markdown("""
        <div style="margin-top:30px;">
        <h3 style="color:#1E8449;">💡 Suggestions to Improve Profile</h3>
        </div>
        """, unsafe_allow_html=True)

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
            st.markdown("""
            <h3 style="color:#2980B9;">📊 Feature Importance</h3>
            """, unsafe_allow_html=True)

            fig, ax = plt.subplots()
            ax.barh(input_data.columns, model.feature_importances_, color="skyblue")
            st.pyplot(fig)

        st.markdown("""
        <h3 style="color:#6C3483; margin-top:30px;">📝 Prediction Summary</h3>
        """, unsafe_allow_html=True)

        st.success(f"""
        - 🧑 Role Applied: **{inputs["job_role_label"]}**
        - 📍 Location: **{inputs["location_label"]}**
        - 💼 Experience: **{inputs["experience"]} years**
        - 🧠 Upskilled: **{inputs["upskilled"]}**
        - 🎯 Result: **{'Selected' if prediction == 1 else 'Not Selected'}** (Confidence: {prob:.2f})
        """)

        input_data["Prediction"] = prediction
        input_data.to_csv("history.csv", mode="a", index=False, header=not os.path.exists("history.csv"))
        if st.button("🔄 Back to Form", use_container_width=True):
            st.session_state.prediction_done = False
            st.rerun()

import pdfplumber
import pytesseract
from PIL import Image
import cv2
import io

# ------------------ ATS Resume Checker ------------------
st.markdown("## 📄 ATS-Friendly Resume Checker")

uploaded_file = st.file_uploader("Upload Resume (PDF or JPG)", type=["pdf", "jpg", "jpeg", "png"])

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def calculate_ats_score(text):
    score = 0
    total = 5

    # Simple checks
    if len(text) > 200: score += 1  # Has enough content
    if any(word in text.lower() for word in ["experience", "skills", "education"]): score += 1  # Keywords
    if len(text.split("\n")) < 60: score += 1  # Not too many lines (structured)
    if not any(word in text.lower() for word in ["table", "image", "photo"]): score += 1  # Avoided visual elements
    if "•" in text or "-" in text: score += 1  # Uses bullet points

    percentage = int((score / total) * 100)
    return percentage

if uploaded_file:
    with st.spinner("🧠 Analyzing Resume..."):
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_image(uploaded_file)

        ats_score = calculate_ats_score(resume_text)
        st.success(f"✅ ATS Friendliness Score: **{ats_score}%**")

        # Suggestions
        st.markdown("### 💡 Suggestions to Improve ATS Score")
        if ats_score < 60:
            st.warning("• Avoid using tables, images, or multi-column layouts.")
            st.warning("• Use clear section titles like 'Experience', 'Education', and 'Skills'.")
            st.warning("• Ensure bullet points and simple fonts are used.")
        elif ats_score < 80:
            st.info("• Good! But consider simplifying layout and using more standard formatting.")
        else:
            st.success("Your resume looks very ATS-friendly! 🚀")

# ---------------------------- Footer ----------------------------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("🔒 *All data processed locally.*")
with col2:
    st.markdown("📧 [Contact Developer](Mail to : 2309poojamurugan@gmail.com (Web Dev) , krithikaarajkumaar@gmail.com (ATS & Chatbot Dev))") 

import pandas as pd
import streamlit as st



# ------------------ Load CSV for Chatbot Context ------------------
@st.cache_data
def load_hiring_data():
    return pd.read_csv('C:/Users/ASUS/Desktop/predictive-hiring-app/dataset/hiring_data.csv')


# ------------------ Cohere Chatbot Integration ------------------
import cohere
import streamlit as st
import pandas as pd

# ✅ Replace with your actual Cohere API key or use st.secrets
co = cohere.Client("xtBhLSqb5EbmwfQe0ylkrdTNgiIvy7JGbR3JgpJS")

# Chatbot function using Cohere
def ask_cohere_chatbot(user_query, df):
    context = df.head(5).to_string(index=False)

    prompt = f"""
You are an AI hiring assistant trained on candidate data.

Here is the data (from uploaded CSV):

{context}

User query: {user_query}

Respond appropriately:
"""

    try:
        response = co.generate(
            model="command-r-plus",  # You can try "command-xlarge-nightly" if supported
            prompt=prompt,
            max_tokens=300,
            temperature=0.5
        )
        return response.generations[0].text.strip()

    except Exception as e:
        return f"❌ Error from Cohere: {str(e)}"

# ------------------ Sidebar Chatbot Toggle ------------------
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

with st.sidebar:
    st.markdown("## 🤖 AI Chatbot")
    st.session_state.show_chat = st.checkbox("💬 Enable Cohere Chatbot")

# ------------------ Display Chatbot UI ------------------
if st.session_state.show_chat:
    st.markdown("""
        <style>
        .chat-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .chat-title {
            font-size: 24px;
            color: #2C3E50;
            margin-bottom: 10px;
        }
        </style>
        <div class="chat-container">
            <div class="chat-title">💬 Ask about Hiring Trends</div>
        </div>
    """, unsafe_allow_html=True)

    # 👇 Make sure this function exists and returns your uploaded CSV
    import os

@st.cache_data
def load_hiring_data():
    # Get the directory of this script
    HERE = os.path.dirname(__file__)
    # Construct the path to the dataset folder at project root
    csv_path = os.path.normpath(
        os.path.join(HERE, "..", "dataset", "hiring_data.csv")
    )
    return pd.read_csv(csv_path)


    user_query = st.text_input("Type your question about hiring insights:")

    if user_query:
        with st.spinner("🤖 Thinking..."):
            answer = ask_cohere_chatbot(user_query, df_chat)
            st.success("✅ Answer:")
            st.markdown(f"**{answer}**")
