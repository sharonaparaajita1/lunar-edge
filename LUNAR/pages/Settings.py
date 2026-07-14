"""
LUNAR — Settings
Dark mode, music toggle, notifications, accent color.
"""

import streamlit as st
from styles.theme import inject_theme
from database import update_user_profile, init_db
from utils.helpers import require_login, refresh_user, logout

st.set_page_config(page_title="Settings · LUNAR", page_icon="⚙️", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>⚙️ Settings</h1>
    <p style="color:#94a3b8; margin:0;">Customise your celestial sanctuary.</p>
</div><hr>
""", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

ACCENT_COLORS = {
    "Cosmic Purple": "#7c3aed",
    "Stellar Blue":  "#3b82f6",
    "Aurora Green":  "#22c55e",
    "Solar Gold":    "#f59e0b",
    "Nebula Pink":   "#ec4899",
    "Comet Teal":    "#06b6d4",
}

with col_left:
    # ── Appearance ─────────────────────────────────────────────────
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">🎨 Appearance</h3>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="lunar-card" style="padding:1.2rem 1.5rem;">', unsafe_allow_html=True)

        current_accent = user.get("accent_color", "#7c3aed")
        accent_options = list(ACCENT_COLORS.keys())
        current_name   = next((k for k, v in ACCENT_COLORS.items() if v == current_accent), accent_options[0])

        new_accent_name = st.radio(
            "Accent Colour",
            accent_options,
            index=accent_options.index(current_name),
        )
        new_accent = ACCENT_COLORS[new_accent_name]

        # Preview swatch
        st.markdown(f"""
        <div style="display:flex; gap:0.5rem; margin:0.5rem 0;">
            {"".join(f'<div style="width:28px;height:28px;border-radius:50%;background:{v};{"box-shadow:0 0 10px " + v + "99;" if v == new_accent else "opacity:0.4;"}"></div>' for v in ACCENT_COLORS.values())}
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Apply Accent Colour", use_container_width=True):
            update_user_profile(user["id"], accent_color=new_accent)
            refresh_user()
            st.toast(f"Accent colour updated to {new_accent_name}! ✦", icon="🎨")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Music / Ambience ───────────────────────────────────────────
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">🎵 Ambience</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lunar-card" style="padding:1.2rem 1.5rem;">
        <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;">
            Enable ambient fantasy music for a more immersive experience.
            (Place an MP3 file at <code style="color:#a78bfa;">assets/music/ambient.mp3</code> to activate.)
        </p>
    </div>
    """, unsafe_allow_html=True)

    music_on = st.toggle("🎵 Enable ambient music", value=st.session_state.get("music_on", False))
    st.session_state["music_on"] = music_on
    if music_on:
        import os
        music_path = os.path.join(os.path.dirname(__file__), "..", "assets", "music", "ambient.mp3")
        if os.path.exists(music_path):
            st.audio(music_path, autoplay=True, loop=True)
        else:
            st.info("🎵 Place an ambient MP3 file at `assets/music/ambient.mp3` to enable background music.")

with col_right:
    # ── Account ────────────────────────────────────────────────────
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">👤 Account</h3>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="lunar-card" style="padding:1.2rem 1.5rem;">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.85rem; color:#94a3b8;">
            <div>Username:</div>  <div style="color:#f1f5f9; font-weight:600;">{user['username']}</div>
            <div>Email:</div>     <div style="color:#f1f5f9;">{user.get('email','')}</div>
            <div>Total XP:</div>  <div style="color:#a78bfa; font-weight:700;">{user.get('xp',0):,}</div>
            <div>Day Streak:</div><div style="color:#f59e0b;">{user.get('streak',0)} 🔥</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Notifications ──────────────────────────────────────────────
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">🔔 Preferences</h3>', unsafe_allow_html=True)
    st.markdown('<div class="lunar-card" style="padding:1.2rem 1.5rem;">', unsafe_allow_html=True)
    notif_quests = st.toggle("Notify on quest completion", value=True)
    notif_xp     = st.toggle("Show XP toasts",             value=True)
    notif_ach    = st.toggle("Notify on achievement unlock", value=True)
    st.session_state["notif_quests"] = notif_quests
    st.session_state["notif_xp"]     = notif_xp
    st.session_state["notif_ach"]    = notif_ach
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Danger Zone ────────────────────────────────────────────────
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#ef4444; font-size:1.1rem; margin-bottom:1rem;">⚠️ Danger Zone</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lunar-card" style="padding:1.2rem 1.5rem; border-color:rgba(239,68,68,0.3);">
        <p style="color:#94a3b8; font-size:0.82rem; margin-bottom:1rem;">
            These actions are <strong style="color:#ef4444;">permanent</strong> and cannot be undone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🗑️ Delete all chat history"):
        st.warning("This will permanently erase all your AI chat messages.")
        if st.button("Confirm — Delete Chat History", type="primary"):
            from database import clear_chat_history
            clear_chat_history(user["id"])
            st.success("Chat history cleared.")

    with st.expander("🚪 Log out of LUNAR"):
        st.info("You will be returned to the login page.")
        if st.button("Confirm — Log Out"):
            logout()
            st.switch_page("pages/Login.py")

# ── About ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.78rem; padding:1rem 0;">
    ✦ LUNAR v1.0 — Your Celestial Productivity Sanctuary ✦<br>
    <span style="font-size:0.7rem;">Built with Python · Streamlit · SQLite · Plotly</span>
</div>
""", unsafe_allow_html=True)
