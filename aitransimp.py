import os
import streamlit as st
import PyPDF2
import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

# ===========================
# 🔐 Setup & Configuration
# ===========================
# Use st.secrets for API Key (add in Streamlit Cloud secrets)
# Example: st.secrets["GEMINI_API_KEY"] = "your-key"
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_FALLBACK_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="AI Personal Finance Assistant", page_icon="💰", layout="wide")

# ===========================
# 🎨 Background Styling (Texture Background)
# ===========================
st.markdown("""
    <style>
    /* Texture background using gradient and noise effect */
    .stApp {
        background: 
            linear-gradient(45deg, #f3f3f3 25%, transparent 25%) -50px 0,
            linear-gradient(45deg, #f3f3f3 25%, transparent 25%) 50px 0,
            linear-gradient(45deg, transparent 75%, #f3f3f3 75%) -50px 0,
            linear-gradient(45deg, transparent 75%, #f3f3f3 75%) 50px 0;
        background-size: 100px 100px;
        background-color: #f0f0f0;
        background-blend-mode: overlay;
        background-attachment: fixed;
    }
    
    /* Keep sidebar readable (default white background) */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===========================
# 💅 Custom CSS
# ===========================
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #00C853;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #e0e0e0;
    margin-bottom: 20px;
}
.result-card {
    background: rgba(255, 255, 255, 0.88);  /* Light readable overlay */
    color: #000;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    backdrop-filter: blur(4px);
}
.success-banner {
    background: linear-gradient(to right, #2E7D32, #1B5E20);
    color: white;
    padding: 15px;
    font-size: 18px;
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===========================
# 📘 Sidebar
# ===========================
st.sidebar.title("ℹ️ How to Use This Tool")
st.sidebar.write("""
1. Upload your UPI statement PDF (Paytm, GPay, PhonePe).  
2. The AI will analyze and summarize your spending.  
3. View insights, trends, and personalized financial tips.  
4. Download your report for future planning. 💼
""")

# ===========================
# 🏷️ Title Section
# ===========================
st.markdown('<h1 class="main-title">💰 AI-Powered Personal Finance Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your UPI Transaction PDF for Smart Financial Insights</p>', unsafe_allow_html=True)

# ===========================
# 📂 File Upload
# ===========================
uploaded_file = st.file_uploader("📂 Upload PDF File", type=["pdf"], help="Only PDF files are supported")

def extract_text_from_pdf(file_path):
    """Extracts text from the uploaded PDF file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# ===========================
# 🧠 Gemini Financial Analysis
# ===========================
def analyze_financial_data(text):
    model = genai.GenerativeModel("models/gemini-pro-latest")
    prompt = f"""
    Analyze the following UPI transaction statement text and generate financial insights.
    Focus on summarizing key patterns, savings potential, top spending categories, and smart money advice.

    TEXT DATA:
    {text}

    Please provide the output in this structured markdown format:
    ## 🧾 Financial Summary
    - Total Income: ₹[Amount]
    - Total Expenses: ₹[Amount]
    - Savings: ₹[Amount]
    - Savings Rate: [X]%

    ## 📊 Spending Overview
    - Top Categories (with approx %):
      - [Category]: [X]%
      - [Category]: [X]%
    - Notable Trends:
      - [Trend 1]
      - [Trend 2]

    ## 💡 Recommendations
    - [Suggestion 1]
    - [Suggestion 2]
    - [Suggestion 3]
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Error processing financial data."

# ===========================
# 📊 Main App Logic
# ===========================
if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from your document..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ Failed to extract text. Ensure the document is not a scanned image PDF.")
    else:
        with st.spinner("🤖 Analyzing your financial data using Gemini..."):
            insights = analyze_financial_data(extracted_text)

        # ===========================
        # 🧭 Tabs for Organization
        # ===========================
        tab1, tab2, tab3 = st.tabs(["📈 Insights", "📊 Visualizations", "🧾 Raw Extracted Text"])

        with tab1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.subheader("📊 Financial Insights Report")
            st.markdown(f'<b>📄 Financial Report for {uploaded_file.name}</b>', unsafe_allow_html=True)
            st.write(insights)
            st.markdown('</div>', unsafe_allow_html=True)

            # Downloadable Insights
            buffer = BytesIO()
            buffer.write(insights.encode())
            st.download_button(
                label="📥 Download Insights as TXT",
                data=buffer.getvalue(),
                file_name="financial_insights.txt",
                mime="text/plain"
            )

        with tab2:
            st.subheader("📊 Expense Visualization (Demo Data)")
            # Placeholder chart until structured parsing is added
            demo_data = pd.DataFrame({
                "Category": ["Food", "Bills", "Shopping", "Travel", "Savings"],
                "Amount": [4500, 2300, 5600, 1800, 3200]
            })
            fig, ax = plt.subplots()
            ax.pie(demo_data["Amount"], labels=demo_data["Category"], autopct="%1.1f%%", startangle=90)
            ax.set_title("Spending Breakdown")
            st.pyplot(fig)

        with tab3:
            st.subheader("📜 Extracted Text Preview")
            st.text_area("Raw Text", extracted_text[:3000], height=300)

        st.markdown('<div class="success-banner">🎉 Analysis Complete! Review your spending habits and plan smarter. 🚀</div>', unsafe_allow_html=True)
        st.balloons()
        

    os.remove(file_path)  # Cleanup temp file
