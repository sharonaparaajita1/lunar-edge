"""
LUNAR — Login / Sign Up
"""

import streamlit as st
from styles.theme import inject_theme
from database import create_user, authenticate_user, init_db
from utils.helpers import set_user, get_user

st.set_page_config(page_title="Login · LUNAR", page_icon="🌙", layout="centered")
init_db()
inject_theme()

# If already logged in, redirect to dashboard
if get_user():
    st.switch_page("app.py")

# ── Stars animation ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp { display:flex; align-items:center; justify-content:center; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 1.5rem;">
    <div style="font-size:3rem; margin-bottom:0.8rem; animation:float 6s ease-in-out infinite;">🌙</div>
    <h1 style="font-size:2.8rem; margin:0 0 0.4rem;">LUNAR</h1>
    <p style="color:#94a3b8; font-size:0.95rem; margin:0;">Enter your celestial sanctuary</p>
</div>
<style>
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(-5deg); }
        50%       { transform: translateY(-15px) rotate(5deg); }
    }
</style>
""", unsafe_allow_html=True)

# ── Tab toggle ───────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    tab_login, tab_signup = st.tabs(["🔑  Login", "✨  Sign Up"])

    # ── LOGIN ───────────────────────────────────────────────────
    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown('<p style="color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;">Welcome back, scholar.</p>', unsafe_allow_html=True)
            email    = st.text_input("✉️  Email", placeholder="your@email.com")
            password = st.text_input("🔒  Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Enter LUNAR ✨", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    user = authenticate_user(email.strip().lower(), password)
                    if user:
                        set_user(user)
                        st.success(f"Welcome back, {user['username']}! 🌙")
                        st.balloons()
                        st.switch_page("app.py")
                    else:
                        st.error("Invalid email or password. The stars do not recognise you.")

    # ── SIGN UP ─────────────────────────────────────────────────
    with tab_signup:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("signup_form"):
            st.markdown('<p style="color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;">Begin your celestial journey.</p>', unsafe_allow_html=True)
            new_username = st.text_input("👤  Username", placeholder="CelestialScholar")
            new_email    = st.text_input("✉️  Email",    placeholder="your@email.com")
            new_password = st.text_input("🔒  Password", type="password", placeholder="Min. 6 characters")
            new_confirm  = st.text_input("🔒  Confirm Password", type="password", placeholder="Repeat password")
            submitted_signup = st.form_submit_button("Create My Sanctuary ✨", use_container_width=True)

            if submitted_signup:
                if not all([new_username, new_email, new_password, new_confirm]):
                    st.error("Please fill in all fields.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif new_password != new_confirm:
                    st.error("Passwords do not match.")
                else:
                    user = create_user(
                        new_username.strip(),
                        new_email.strip().lower(),
                        new_password
                    )
                    if user:
                        set_user(user)
                        st.success(f"Welcome to LUNAR, {user['username']}! Your journey begins. 🌙")
                        st.balloons()
                        st.switch_page("app.py")
                    else:
                        st.error("That email or username is already taken. Try a different one.")

# ── Footer ───────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3rem; color:#334155; font-size:0.75rem;">
    ✦ LUNAR v1.0 — Your Celestial Productivity Sanctuary ✦
</div>
""", unsafe_allow_html=True)
