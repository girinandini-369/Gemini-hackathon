import streamlit as st
import requests
import time
import pandas as pd
import os

# ---------------------------
# Get Gemini API key
# ---------------------------
gemini_key = os.getenv("AIzaSyB23xK3uGeCJ_Fv3DuvW5QKHhA0_oTSPDs")  # for Streamlit Cloud
if gemini_key is None:
    try:
        with open("key.txt") as f:
            gemini_key = f.read().strip()  # fallback for local testing
    except FileNotFoundError:
        gemini_key = None

# ---------------------------
# Mock Gemini AI function
# ---------------------------
def mock_gemini_analysis(logs):
    # Simple sample analysis for demo/hackathon
    issues = []
    for log in logs:
        if log["Status"] != "✅ Success":
            issues.append(f"Call #{log['Call']} failed. Check API or increase timeout.")
    if not issues:
        return "All API calls successful. No issues detected!"
    return "\n".join(issues)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="AI Pulse-API Health Monitor", layout="wide")
st.title("AI Pulse-API Health Monitor 🚀")
st.markdown("""
Monitor your APIs in real-time, predict failures, and get AI-based suggestions (mocked) for hackathon demo!
""")

# Inputs
api_url = st.text_input("Enter API URL to monitor:", "https://jsonplaceholder.typicode.com/posts")
interval = st.slider("Monitoring interval (seconds):", min_value=1, max_value=10, value=3)
start = st.button("Start Monitoring")

# Data storage
if 'log_data' not in st.session_state:
    st.session_state['log_data'] = []

if start:
    st.session_state['log_data'] = []
    st.success(f"Monitoring started for {api_url} every {interval} seconds.")

    placeholder = st.empty()
    analysis_placeholder = st.empty()

    for i in range(10):
        try:
            start_time = time.time()
            response = requests.get(api_url, timeout=interval)
            latency = round((time.time() - start_time) * 1000, 2)
            status = "✅ Success" if response.status_code == 200 else f"❌ {response.status_code}"
        except requests.exceptions.Timeout:
            latency = None
            status = "⏱️ Timeout"
        except Exception as e:
            latency = None
            status = f"❌ Error: {e}"

        st.session_state['log_data'].append({"Call": i+1, "Status": status, "Latency_ms": latency})

        # Display last 5 calls in cards with dark colors
        logs_html = ""
        for log in st.session_state['log_data'][-5:]:
            if "Success" in log['Status']:
                color = "#2E7D32"  # dark green
            elif "Timeout" in log['Status']:
                color = "#616161"  # dark gray
            else:
                color = "#C62828"  # dark red
            logs_html += f"""
            <div style="background-color:{color}; padding:12px; border-radius:12px; margin-bottom:6px; color:white; font-weight:bold;">
                Call #{log['Call']}<br>
                Status: {log['Status']}<br>
                Latency: {log['Latency_ms'] if log['Latency_ms'] else 'N/A'} ms
            </div>
            """
        placeholder.markdown(logs_html, unsafe_allow_html=True)

        time.sleep(interval)

    # Mock Gemini AI analysis
    analysis = mock_gemini_analysis(st.session_state['log_data'])
    analysis_placeholder.markdown(f"### 🔍 AI Analysis (Mocked)\n{analysis}")

    # Full log table
    st.markdown("### 📊 Full API Log Table")
    df = pd.DataFrame(st.session_state['log_data'])
    st.dataframe(df, use_container_width=True)

st.markdown("Developed for Gemini Hackathon | Powered by Mocked AI Suggestions 🚀")
