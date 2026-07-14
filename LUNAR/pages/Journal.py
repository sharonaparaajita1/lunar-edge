"""
LUNAR — Journal
Daily journal with mood tracker and writing streak.
"""

import streamlit as st
from datetime import date
from styles.theme import inject_theme
from database import (get_journal_entry, upsert_journal_entry, get_journal_entries,
                      get_journal_streak, update_user_xp, check_and_unlock_achievements, init_db)
from utils.helpers import require_login, refresh_user, empty_state, format_date, today_str, toast_xp
from config import MOODS, MOOD_LABELS, XP_PER_JOURNAL

st.set_page_config(page_title="Journal · LUNAR", page_icon="✍️", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>✍️ Journal</h1>
    <p style="color:#94a3b8; margin:0;">Reflect. Grow. Chronicle your celestial journey.</p>
</div><hr>
""", unsafe_allow_html=True)

PROMPTS = [
    "What did you learn today that surprised you?",
    "What is one thing you are grateful for right now?",
    "What challenge are you currently facing, and how might you overcome it?",
    "Describe a moment today when you felt most alive.",
    "What would you do differently if you could relive today?",
    "What is one step you can take tomorrow to move closer to your goals?",
    "What has been occupying your mind lately?",
    "Who inspired you today, and why?",
]

col_write, col_history = st.columns([3, 2])

with col_write:
    streak = get_journal_streak(user["id"])
    entries = get_journal_entries(user["id"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{streak}🔥</div><div class="metric-label">Writing Streak</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(entries)}</div><div class="metric-label">Total Entries</div></div>', unsafe_allow_html=True)
    with c3:
        import random
        today_entry = get_journal_entry(user["id"], today_str())
        wrote_today = "✓ Yes" if today_entry and today_entry.get("content") else "✗ No"
        color = "#22c55e" if today_entry and today_entry.get("content") else "#ef4444"
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{color};">{wrote_today}</div><div class="metric-label">Wrote Today</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Date selector
    selected_date = st.date_input("📅 Entry date", value=date.today())
    date_str = selected_date.isoformat()
    existing = get_journal_entry(user["id"], date_str)

    # Mood selector
    st.markdown('<p style="color:#94a3b8; font-size:0.85rem; margin-bottom:0.4rem;">💫 How are you feeling?</p>', unsafe_allow_html=True)
    current_mood = existing["mood"] if existing else 2
    mood_cols = st.columns(5)
    selected_mood = current_mood
    for i, (emoji, label) in enumerate(zip(MOODS, MOOD_LABELS)):
        with mood_cols[i]:
            sel = (i == current_mood)
            border = "border:2px solid #7c3aed; background:rgba(124,58,237,0.2);" if sel else "border:1px solid rgba(255,255,255,0.08);"
            st.markdown(f"""
            <div style="text-align:center; {border} border-radius:10px; padding:0.6rem 0.2rem; cursor:pointer;">
                <div style="font-size:1.5rem;">{emoji}</div>
                <div style="font-size:0.6rem; color:#94a3b8; margin-top:0.2rem;">{label}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"{i}", key=f"j_mood_{i}", label_visibility="collapsed"):
                selected_mood = i

    # Reflection prompt
    import hashlib
    prompt_idx = int(hashlib.md5(date_str.encode()).hexdigest(), 16) % len(PROMPTS)
    st.markdown(f"""
    <div class="lunar-card" style="padding:0.8rem 1.2rem; margin:1rem 0;">
        <p style="color:#a78bfa; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 0.4rem;">✦ Today's Reflection Prompt</p>
        <p style="color:#e2e8f0; font-size:0.9rem; font-style:italic; margin:0;">"{PROMPTS[prompt_idx]}"</p>
    </div>
    """, unsafe_allow_html=True)

    # Journal editor
    default_content = existing["content"] if existing else ""
    with st.form("journal_form"):
        content = st.text_area(
            "Your thoughts",
            value=default_content,
            height=280,
            placeholder="Begin writing your celestial chronicle...\n\nLet your thoughts flow freely. This is your sacred space.",
            label_visibility="collapsed"
        )
        save_col, hint_col = st.columns([1, 3])
        with save_col:
            save_btn = st.form_submit_button("💾 Save Entry", use_container_width=True)
        with hint_col:
            word_count = len(content.split()) if content.strip() else 0
            st.markdown(f'<p style="color:#475569; font-size:0.78rem; margin:0.6rem 0 0;">{word_count} words</p>', unsafe_allow_html=True)

        if save_btn:
            if not content.strip():
                st.warning("Write something before saving — even a few words count.")
            else:
                upsert_journal_entry(user["id"], date_str, selected_mood, content)
                if not existing or not existing.get("content"):
                    update_user_xp(user["id"], XP_PER_JOURNAL)
                    check_and_unlock_achievements(user["id"])
                    refresh_user()
                    toast_xp(XP_PER_JOURNAL, "Journal entry saved")
                else:
                    st.toast("Entry updated! ✦", icon="✍️")
                st.rerun()

with col_history:
    st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem; margin-bottom:1rem;">📜 Past Entries</h3>', unsafe_allow_html=True)
    all_entries = get_journal_entries(user["id"])

    if not all_entries:
        empty_state("📜", "No Entries Yet", "Begin your celestial chronicle today.")
    else:
        for entry in all_entries[:15]:
            mood_emoji = MOODS[entry["mood"]] if 0 <= entry["mood"] < len(MOODS) else "😐"
            mood_label = MOOD_LABELS[entry["mood"]] if 0 <= entry["mood"] < len(MOOD_LABELS) else ""
            preview    = entry["content"][:100] + "..." if len(entry["content"]) > 100 else entry["content"]
            is_today   = entry["entry_date"] == today_str()

            st.markdown(f"""
            <div class="lunar-card" style="padding:0.9rem 1.1rem; {'border-color:rgba(124,58,237,0.5);' if is_today else ''}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                    <span style="font-size:0.75rem; color:#94a3b8;">
                        {format_date(entry['entry_date'])}{'  ✦ Today' if is_today else ''}
                    </span>
                    <span title="{mood_label}" style="font-size:1.1rem;">{mood_emoji}</span>
                </div>
                <p style="color:#e2e8f0; font-size:0.82rem; line-height:1.5; margin:0; font-style:italic;">
                    "{preview}"
                </p>
            </div>
            """, unsafe_allow_html=True)
