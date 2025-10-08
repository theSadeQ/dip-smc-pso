# Example from: docs\deployment\STREAMLIT_DEPLOYMENT.md
# Index: 1
# Runnable: True
# Hash: 0cea67ca

# Add to streamlit_app.py for custom health endpoint
import streamlit as st

if st.sidebar.button("Health Check"):
    st.success("✅ Application is running normally")
    st.info(f"Cache size: {len(st.session_state)} items")