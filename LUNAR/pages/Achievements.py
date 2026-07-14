"""
LUNAR — Achievements
Unlock badges and milestones.
"""

import streamlit as st
from styles.theme import inject_theme
from database import get_unlocked_achievements, check_and_unlock_achievements, init_db, get_analytics
from utils.helpers import require_login, refresh_user, format_date
from config import ACHIEVEMENTS

st.set_page_config(page_title="Achievements · LUNAR", page_icon="🏆", layout="wide")
init_db()
inject_theme()

user = require_login()

# Check for newly unlocked achievements
new_ach = check_and_unlock_achievements(user["id"])
if new_ach:
    refresh_user()
    for _ in new_ach:
        st.toast("🏆 New Achievement Unlocked!", icon="🌟")

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>🏆 Achievements</h1>
    <p style="color:#94a3b8; margin:0;">Your milestones of celestial mastery.</p>
</div><hr>
""", unsafe_allow_html=True)

unlocked_ids = get_unlocked_achievements(user["id"])
unlocked_set = set(unlocked_ids)

total       = len(ACHIEVEMENTS)
unlocked_n  = len(unlocked_ids)
locked_n    = total - unlocked_n
pct         = int(unlocked_n / total * 100) if total else 0

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{unlocked_n}</div><div class="metric-label">Unlocked</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{locked_n}</div><div class="metric-label">Locked</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{pct}%</div><div class="metric-label">Complete</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.progress(pct / 100)
st.markdown("<br>", unsafe_allow_html=True)

# Filter
filter_col1, filter_col2 = st.columns([3, 1])
with filter_col2:
    show_only = st.selectbox("Show", ["All", "Unlocked", "Locked"], label_visibility="collapsed")

filtered = ACHIEVEMENTS
if show_only == "Unlocked":
    filtered = [a for a in ACHIEVEMENTS if a["id"] in unlocked_set]
elif show_only == "Locked":
    filtered = [a for a in ACHIEVEMENTS if a["id"] not in unlocked_set]

# Grid
cols = st.columns(4)
for i, ach in enumerate(filtered):
    with cols[i % 4]:
        is_unlocked = ach["id"] in unlocked_set
        card_class  = "ach-card-unlocked" if is_unlocked else "ach-card-locked"
        xp_text     = f'+{ach["xp_reward"]} XP' if ach.get("xp_reward") else ""

        st.markdown(f"""
        <div class="{card_class}">
            <div class="ach-icon">{ach['icon']}</div>
            <div class="ach-name">{ach['name']}</div>
            <div class="ach-desc">{ach['desc']}</div>
            {f'<div style="color:#fde68a; font-size:0.7rem; margin-top:0.5rem; font-weight:600;">{xp_text}</div>' if xp_text else ''}
            {f'<div style="color:#22c55e; font-size:0.65rem; margin-top:0.3rem;">✓ Unlocked</div>' if is_unlocked else '<div style="color:#475569; font-size:0.65rem; margin-top:0.3rem;">🔒 Locked</div>'}
        </div>
        <div style="margin-bottom:0.8rem;"></div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="lunar-card" style="padding:1rem 1.5rem;">
    <h4 style="font-family:'Cinzel',serif; color:#a78bfa; margin-bottom:0.6rem; font-size:0.9rem;">✦ How to Unlock</h4>
    <p style="color:#64748b; font-size:0.82rem; line-height:1.7; margin:0;">
        Achievements unlock automatically as you use LUNAR. Log in daily, write journal entries,
        add library items, build habits, and earn XP through quests. Every action brings you
        closer to the next milestone. Keep going — the stars are watching.
    </p>
</div>
""", unsafe_allow_html=True)
