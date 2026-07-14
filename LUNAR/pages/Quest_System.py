"""
LUNAR — Quest System
Daily and weekly quests with XP rewards.
"""

import streamlit as st
from styles.theme import inject_theme
from database import get_quests, complete_quest, seed_quests, check_and_unlock_achievements, init_db, get_user_by_id
from utils.helpers import require_login, refresh_user, empty_state, toast_xp
from config import MOODS

st.set_page_config(page_title="Quests · LUNAR", page_icon="⚔️", layout="wide")
init_db()
inject_theme()

user = require_login()

# Seed quests for today/this week if needed
seed_quests(user["id"])

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>⚔️ Quest System</h1>
    <p style="color:#94a3b8; margin:0;">Complete quests. Earn XP. Rise through the celestial ranks.</p>
</div><hr>
""", unsafe_allow_html=True)

# XP summary
user = get_user_by_id(user["id"])
daily_quests  = get_quests(user["id"], "daily")
weekly_quests = get_quests(user["id"], "weekly")
daily_done    = sum(1 for q in daily_quests  if q["completed"])
weekly_done   = sum(1 for q in weekly_quests if q["completed"])
total_xp_today = sum(q["xp_reward"] for q in daily_quests  if q["completed"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{user["xp"]:,}</div><div class="metric-label">Total XP</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{daily_done}/{len(daily_quests)}</div><div class="metric-label">Daily Done</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{weekly_done}/{len(weekly_quests)}</div><div class="metric-label">Weekly Done</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">+{total_xp_today}</div><div class="metric-label">XP Today</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_daily, col_weekly = st.columns(2)

CATEGORY_ICONS = {"Study": "📚", "Library": "📖", "Journal": "✍️", "Habits": "⚡"}


def render_quest_card(q: dict, key_prefix: str) -> None:
    done     = bool(q["completed"])
    cat_icon = CATEGORY_ICONS.get(q["category"], "✦")
    opacity  = "opacity:0.45;" if done else ""
    glow     = "box-shadow: 0 0 20px rgba(124,58,237,0.2); border-color:rgba(124,58,237,0.4);" if not done else ""
    check    = "✅" if done else "○"

    st.markdown(f"""
    <div class="lunar-card" style="padding:1rem 1.2rem; {opacity} {glow}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <span style="font-size:1.2rem;">{cat_icon}</span>
                <span style="font-weight:600; color:#e2e8f0; font-size:0.9rem; line-height:1.4;">
                    {q['name']}
                </span>
            </div>
            <span style="font-size:1.2rem; flex-shrink:0;">{check}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="lunar-badge badge-purple">{q['category']}</span>
            <span style="color:#fde68a; font-weight:700; font-size:0.9rem;">+{q['xp_reward']} XP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not done:
        if st.button(f"Complete Quest ✓", key=f"{key_prefix}_{q['id']}", use_container_width=True):
            earned = complete_quest(q["id"], user["id"])
            check_and_unlock_achievements(user["id"])
            refresh_user()
            toast_xp(earned, q["name"])
            st.rerun()
    else:
        st.markdown('<p style="color:#22c55e; font-size:0.78rem; text-align:center; margin:0;">Quest Complete ✓</p>', unsafe_allow_html=True)


with col_daily:
    st.markdown("""
    <h3 style="font-family:'Cinzel',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">
        🌅 Daily Quests
        <span style="font-size:0.7rem; color:#64748b; margin-left:0.5rem;">Resets at midnight</span>
    </h3>
    """, unsafe_allow_html=True)

    if not daily_quests:
        empty_state("⚔️", "No Daily Quests", "Come back tomorrow for new quests!")
    else:
        for q in daily_quests:
            render_quest_card(q, "dq")

with col_weekly:
    st.markdown("""
    <h3 style="font-family:'Cinzel',serif; color:#f59e0b; font-size:1.1rem; margin-bottom:1rem;">
        🌟 Weekly Challenges
        <span style="font-size:0.7rem; color:#64748b; margin-left:0.5rem;">Resets Monday</span>
    </h3>
    """, unsafe_allow_html=True)

    if not weekly_quests:
        empty_state("🌟", "No Weekly Quests", "New challenges reset each Monday.")
    else:
        for q in weekly_quests:
            render_quest_card(q, "wq")

# How quests work
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="lunar-card" style="padding:1.2rem 1.5rem;">
    <h4 style="font-family:'Cinzel',serif; color:#a78bfa; margin-bottom:0.8rem; font-size:0.95rem;">✦ How Quests Work</h4>
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:1rem; color:#94a3b8; font-size:0.82rem; line-height:1.6;">
        <div>📚 <strong style="color:#e2e8f0;">Study Quests</strong><br>Complete tasks or use the Study Planner</div>
        <div>📖 <strong style="color:#e2e8f0;">Library Quests</strong><br>Add books, articles, or notes</div>
        <div>✍️ <strong style="color:#e2e8f0;">Journal Quests</strong><br>Write daily reflections</div>
        <div>⚡ <strong style="color:#e2e8f0;">Habit Quests</strong><br>Mark habits as complete</div>
    </div>
</div>
""", unsafe_allow_html=True)
