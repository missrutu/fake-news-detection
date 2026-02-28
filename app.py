import streamlit as st
import pickle
import base64
import matplotlib.pyplot as plt

st.set_page_config(page_title="TruthGuard AI", layout="centered")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "count" not in st.session_state:
    st.session_state.count = 0

# ---------------- BACKGROUND + STYLING ----------------
def set_bg(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .card {{
            background: rgba(255,255,255,0.15);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            animation: fadeIn 1.2s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{opacity: 0; transform: translateY(20px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}

        .stButton>button {{
            background: linear-gradient(45deg, #ff4b4b, #ff884b);
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            border: none;
            transition: 0.3s ease;
        }}

        .stButton>button:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}

        .typing {{
            font-size: 32px;
            font-weight: bold;
            border-right: 3px solid;
            white-space: nowrap;
            overflow: hidden;
            width: 0;
            animation: typing 3s steps(30, end) forwards,
                       blink 0.7s infinite;
        }}

        @keyframes typing {{
            from {{ width: 0 }}
            to {{ width: 100% }}
        }}

        @keyframes blink {{
            50% {{ border-color: transparent }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- LOGIN PAGE ----------------
def login_page():
    set_bg("light_bg.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.title("🔐 TruthGuard AI Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
def dashboard():

    st.sidebar.title("⚙ Controls")

    theme = st.sidebar.radio("Theme", ["Light ☀", "Dark 🌙"])

    if theme == "Dark 🌙":
        set_bg("dark_bg.jpg")
    else:
        set_bg("light_bg.jpg")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="typing">🧠 TruthGuard AI Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Accuracy", "98%")
    col2.metric("Algorithm", "Logistic Regression")
    col3.metric("Predictions", st.session_state.count)

    st.markdown("---")

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    user_input = st.text_area("Enter News Text")

    if st.button("Analyze"):

        if user_input.strip() == "":
            st.warning("Please enter text.")
        else:
            with st.spinner("Analyzing News with AI Model..."):

                input_data = vectorizer.transform([user_input])
                prediction = model.predict(input_data)
                probability = model.predict_proba(input_data)

                st.session_state.count += 1

                confidence = max(probability[0]) * 100

            if prediction[0] == 0:
                st.error("❌ FAKE News Detected")
            else:
                st.success("✅ REAL News")

            st.progress(int(confidence))
            st.info(f"Confidence: {confidence:.2f}%")

            st.subheader("📊 Probability Chart")

            fig, ax = plt.subplots()
            labels = ["Fake", "Real"]
            ax.bar(labels, probability[0])
            st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()