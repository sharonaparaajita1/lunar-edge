"""
LUNAR — Profile
Avatar, bio, statistics, achievements.
"""

import streamlit as st
from styles.theme import inject_theme
from database import (get_user_by_id, update_user_profile, get_analytics,
                      get_unlocked_achievements, init_db)
from utils.helpers import require_login, refresh_user, xp_bar
from config import ACHIEVEMENTS, get_level_title, HABIT_COLORS

st.set_page_config(page_title="Profile · LUNAR", page_icon="👤", layout="wide")
init_db()
inject_theme()

user = require_login()
user = get_user_by_id(user["id"])  # Fresh data

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>👤 Profile</h1>
    <p style="color:#94a3b8; margin:0;">Your celestial identity and journey.</p>
</div><hr>
""", unsafe_allow_html=True)

col_profile, col_stats = st.columns([1, 2])

with col_profile:
    avatar_color = user.get("avatar_color", "#7c3aed")
    level, title_lbl, xp_floor, xp_ceil = get_level_title(user.get("xp", 0))

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="width:100px; height:100px; border-radius:50%;
                    background:linear-gradient(135deg,{avatar_color},{user.get('accent_color','#4f46e5')});
                    display:flex; align-items:center; justify-content:center;
                    font-size:2.8rem; font-weight:700; color:white; margin:0 auto 1rem;
                    box-shadow: 0 0 30px {avatar_color}66, 0 0 60px {avatar_color}33;">
            {user['username'][0].upper()}
        </div>
        <h2 style="font-family:'Cinzel',serif; font-size:1.5rem; margin:0 0 0.3rem; color:#f1f5f9;">{user['username']}</h2>
        <div class="lunar-badge badge-gold">Lv.{level} · {title_lbl}</div>
        <p style="color:#64748b; font-size:0.82rem; margin:0.8rem 0 0;">{user.get('email','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="lunar-card" style="text-align:center;">
        <p style="color:#94a3b8; font-size:0.8rem; font-style:italic; margin:0;">
            "{user.get('bio') or 'No bio yet — add one below!'}"
        </p>
    </div>
    """, unsafe_allow_html=True)

    xp_bar(user.get("xp", 0))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.8rem;">✏️ Edit Profile</h4>', unsafe_allow_html=True)

    with st.form("edit_profile"):
        new_username = st.text_input("Username", value=user["username"])
        new_bio      = st.text_area("Bio", value=user.get("bio",""), placeholder="Tell the cosmos who you are...", height=80)

        st.markdown('<p style="color:#64748b; font-size:0.8rem; margin-bottom:0.3rem;">Avatar Colour</p>', unsafe_allow_html=True)
        new_color = st.selectbox("Avatar Colour", HABIT_COLORS, index=HABIT_COLORS.index(avatar_color) if avatar_color in HABIT_COLORS else 0, label_visibility="collapsed")

        if st.form_submit_button("💾 Save Changes", use_container_width=True):
            if not new_username.strip():
                st.error("Username cannot be empty.")
            else:
                update_user_profile(user["id"], username=new_username.strip(), bio=new_bio, avatar_color=new_color)
                refresh_user()
                st.toast("Profile updated! ✦", icon="✨")
                st.rerun()

with col_stats:
    data = get_analytics(user["id"])
    stats = [
        ("📋", "Total Tasks",     data["total_tasks"]),
        ("✅", "Completed Tasks", data["completed_tasks"]),
        ("📚", "Library Items",   data["total_library"]),
        ("✍️", "Journal Entries", data["total_journal"]),
        ("⚡", "Active Habits",   data["total_habits"]),
        ("📝", "Notes Created",   data["total_notes"]),
        ("🔥", "Day Streak",      user.get("streak", 0)),
        ("⭐", "Total XP",        f'{user.get("xp", 0):,}'),
    ]

    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">📊 Your Stats</h3>', unsafe_allow_html=True)
    sc = st.columns(4)
    for i, (icon, label, val) in enumerate(stats):
        with sc[i % 4]:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:0.8rem;">
                <div style="font-size:1.3rem; margin-bottom:0.3rem;">{icon}</div>
                <div class="metric-value" style="font-size:1.4rem;">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">🏆 Achievements</h3>', unsafe_allow_html=True)

    unlocked_ids = set(get_unlocked_achievements(user["id"]))
    unlocked_ach = [a for a in ACHIEVEMENTS if a["id"] in unlocked_ids]

    if not unlocked_ach:
        st.markdown('<p style="color:#475569; font-size:0.85rem;">No achievements yet. Complete quests and build habits to earn them!</p>', unsafe_allow_html=True)
    else:
        ach_cols = st.columns(min(4, len(unlocked_ach)))
        for i, ach in enumerate(unlocked_ach):
            with ach_cols[i % 4]:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3);
                            border-radius:12px; padding:0.8rem 0.5rem; margin-bottom:0.5rem;">
                    <div style="font-size:1.8rem;">{ach['icon']}</div>
                    <div style="font-family:'Cinzel',serif; font-size:0.7rem; color:#fde68a; margin-top:0.3rem;">{ach['name']}</div>
                </div>
                """, unsafe_allow_html=True)
