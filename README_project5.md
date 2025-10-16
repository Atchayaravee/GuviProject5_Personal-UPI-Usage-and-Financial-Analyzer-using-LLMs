# 💰 AI-Powered UPI Transaction Analyzer

An intelligent personal finance assistant built with **Streamlit** and **Gemini LLM** that analyzes UPI transaction statements (Paytm, GPay, PhonePe, etc.) and provides smart financial insights, spending analysis, and personalized recommendations — all in a clean, interactive dashboard.

## 🧠 Problem Statement
UPI usage has grown exponentially, but users often lack clarity on their spending behavior, savings patterns, and financial health.
This project solves the problem by:
- Parsing UPI transaction statements from different apps.
- Structuring the data for analysis.
- Generating actionable financial insights and budgeting tips using LLMs.
- Providing a simple, elegant UI to explore spending habits.

## 🚀 Key Features
- 📄 PDF Parsing from Paytm, GPay, PhonePe.
- 🧮 Spending Summary: income, expenses, savings.
- 📊 Category Analysis with pie chart.
- 🧠 AI Insights using Gemini.
- 📥 Exportable reports.

## 🏗️ Tech Stack
- Frontend: Streamlit
- Backend: Google Gemini
- Data: PyPDF2, Pandas
- Visualization: Matplotlib
- Language: Python 3.10+

## 🧭 Project Workflow
1. Upload UPI statement PDF.
2. Extract text using PyPDF2.
3. Clean and structure data.
4. Use Gemini to generate insights.
5. Visualize results and export.

## 🧪 Installation
```bash
git clone https://github.com/your-username/upi-transaction-analyzer.git
cd upi-transaction-analyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
Add your Gemini API key in `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_key_here"
```
Run the app:
```bash
streamlit run app.py
```

## 🧾 Sample Output
```
## 🧾 Financial Summary
- Total Income: ₹12,000
- Total Expenses: ₹9,500
- Savings: ₹2,500
- Savings Rate: 20.8%

## 📊 Spending Overview
- Top Categories:
  - Food: 38%
  - Shopping: 25%
  - Bills: 20%
- Notable Trends:
  - High weekend spending
  - Frequent small-value transactions

## 💡 Recommendations
- Reduce impulse weekend spending
- Set monthly cap on shopping
- Automate savings of ₹2,000/month
```

## 🧾 Future Enhancements
- OCR support for scanned PDFs
- Merchant-level insights
- Budget alerts and forecasting
- Advanced visualizations

## 🤝 Contributing
Pull requests are welcome!

## 🛡️ License
MIT License

## ✨ Acknowledgements
- Google Gemini
- Streamlit
- PyPDF2
- Matplotlib
