import streamlit as st
from auth import register_user, authenticate_user

st.set_page_config(page_title="Login", layout="centered")

if "user" not in st.session_state:
    st.session_state["user"] = None

st.title("Sign in / Register")

tab1, tab2 = st.tabs(["Sign in", "Register"])
with tab1:
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Sign in"):
        if authenticate_user(username, password):
            st.session_state["user"] = username
            st.success("Signed in")
            st.query_params["page"] = "D:\Personalised-Mental-Health-Analysis-and-Support\app.py" 
            st.rerun()
        else:
            st.error("Invalid credentials")

with tab2:
    r_username = st.text_input("Choose username", key="reg_username")
    r_password = st.text_input("Choose password", type="password", key="reg_password")
    if st.button("Register"):
        ok = register_user(r_username, r_password)
        if ok:
            st.success("User registered — please sign in")
        else:
            st.error("Username taken")