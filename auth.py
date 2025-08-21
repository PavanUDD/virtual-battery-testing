import streamlit as st

# Simple user system (demo only)
USERS = {
    "admin": "password123",
    "guest": "demo"
}

def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["auth"] = True
            st.session_state["user"] = username
        else:
            st.error("Invalid username or password")

def check_auth():
    return st.session_state.get("auth", False)
