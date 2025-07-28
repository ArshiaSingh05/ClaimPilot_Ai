import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from evaluate_decision import evaluate_claim
import os

st.title("🛡️ Health Insurance Clause Evaluator")

# Upload the PDF
uploaded_pdf = st.file_uploader(" Upload your Health Insurance Policy (PDF)", type=["pdf"])

# Once uploaded
if uploaded_pdf is not None:
    # Save PDF to 'data/' folder
    os.makedirs("data", exist_ok=True)
    pdf_path = os.path.join("data", uploaded_pdf.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())
    
    st.success(f" Uploaded: {uploaded_pdf.name}")

    # Extract text
    with st.spinner(" Extracting content..."):
        raw_text = extract_text_from_pdf(pdf_path)
        st.success(" PDF extracted and ready.")

    # User query input
    user_query = st.text_input(" Enter your query (e.g., 'Need claim for surgery in Mumbai last month')")

    if user_query:
        with st.spinner(" Evaluating..."):
            result = evaluate_claim(user_query, context=raw_text)
            st.subheader(" Claim Decision")
            st.json(result)
