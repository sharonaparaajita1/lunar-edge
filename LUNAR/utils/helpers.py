"""
LUNAR Utility Helpers
Shared functions used across all pages.
"""

from datetime import date, timedelta
from typing import Any
import streamlit as st


# ── Session state ─────────────────────────────────────────────────

def get_user() -> dict | None:
    """Return the current logged-in user dict, or None."""
    return st.session_state.get("user")


def require_login() -> dict:
    """Redirect to login if not authenticated; else return user."""
    user = get_user()
    if not user:
        st.warning("Please log in to continue.")
        st.page_link("pages/Login.py", label="Go to Login", icon="🔑")
        st.stop()
    return user


def set_user(user: dict) -> None:
    st.session_state["user"] = user


def logout() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def refresh_user() -> None:
    """Re-fetch the current user from DB and update session."""
    from database import get_user_by_id
    user = get_user()
    if user:
        updated = get_user_by_id(user["id"])
        if updated:
            st.session_state["user"] = updated


# ── Date helpers ──────────────────────────────────────────────────

def today_str() -> str:
    return date.today().isoformat()


def last_n_days(n: int = 7) -> list[str]:
    """Return the last N dates as ISO strings, oldest first."""
    return [(date.today() - timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


def format_date(iso: str) -> str:
    """Format ISO date string as 'Mon DD, YYYY'."""
    try:
        return date.fromisoformat(iso[:10]).strftime("%b %d, %Y")
    except Exception:
        return iso


def format_datetime(iso: str) -> str:
    """Format ISO datetime string."""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%b %d, %Y  %H:%M")
    except Exception:
        return iso


# ── XP / Level ────────────────────────────────────────────────────

def xp_bar(xp: int) -> None:
    """Render an XP progress bar with level info."""
    from config import get_level_title
    level, title, xp_floor, xp_ceil = get_level_title(xp)
    progress = (xp - xp_floor) / max(xp_ceil - xp_floor, 1)
    st.markdown(f"""
    <div style="margin-bottom:0.5rem;">
        <span style="font-family:'Cinzel',serif; color:#a78bfa; font-size:0.9rem;">
            Lv.{level} · {title}
        </span>
        <span style="float:right; color:#94a3b8; font-size:0.8rem;">{xp} XP</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(min(progress, 1.0))
    st.markdown(f"""
    <div style="color:#64748b; font-size:0.72rem; text-align:right; margin-top:-0.5rem;">
        {xp - xp_floor} / {xp_ceil - xp_floor} XP to next level
    </div>
    """, unsafe_allow_html=True)


# ── Colour helpers ────────────────────────────────────────────────

PRIORITY_COLORS = {
    "High":   ("#ef4444", "red"),
    "Medium": ("#f59e0b", "gold"),
    "Low":    ("#22c55e", "green"),
}

SUBJECT_COLORS = {
    "Mathematics":  "#3b82f6",
    "Science":      "#22c55e",
    "Literature":   "#a855f7",
    "History":      "#f59e0b",
    "Programming":  "#06b6d4",
    "Languages":    "#ec4899",
    "Arts":         "#f97316",
    "Other":        "#94a3b8",
}

HABIT_COLORS = [
    "#7c3aed", "#3b82f6", "#22c55e", "#f59e0b",
    "#ec4899", "#06b6d4", "#f97316", "#a855f7",
]


def priority_badge_html(priority: str) -> str:
    color, cls = PRIORITY_COLORS.get(priority, ("#94a3b8", "purple"))
    return f'<span style="color:{color}; background:rgba(0,0,0,0.3); border:1px solid {color}40; border-radius:999px; padding:2px 8px; font-size:0.7rem; font-weight:600;">{priority}</span>'


# ── Toast / feedback ──────────────────────────────────────────────

def toast_xp(amount: int, reason: str = "") -> None:
    msg = f"✨ +{amount} XP"
    if reason:
        msg += f" — {reason}"
    st.toast(msg, icon="⭐")


# ── Empty states ──────────────────────────────────────────────────

def empty_state(icon: str, title: str, message: str) -> None:
    st.markdown(f"""
    <div style="text-align:center; padding:3rem 1rem; opacity:0.6;">
        <div style="font-size:3rem; margin-bottom:1rem;">{icon}</div>
        <h3 style="color:#a78bfa; font-family:'Cinzel',serif; margin-bottom:0.5rem;">{title}</h3>
        <p style="color:#64748b; font-size:0.9rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


# ── AI response generator ─────────────────────────────────────────

import random

WISDOM_QUOTES = [
    "The stars do not ask why they shine — they simply do. Let your learning be the same.",
    "Every page turned is a spell cast upon the universe. Keep reading, keep growing.",
    "In the library of the cosmos, your curiosity is the most powerful spell.",
    "The moon does not compete with the sun. Find your own rhythm.",
    "Small habits, like constellations, form the greatest patterns over time.",
    "A question asked is a door opened. Keep asking.",
    "The universe is not made of atoms — it is made of tiny stories. Write yours.",
    "Progress, not perfection, is the magic word.",
    "Discipline is the bridge between your goals and your achievements.",
    "You are not studying to pass tests — you are studying to change the shape of your mind.",
]

AI_RESPONSES: dict[str, str] = {
    "hello":      "Greetings, celestial scholar! 🌙 The moon watches over your studies tonight. How may I illuminate your path?",
    "help":       "I am LUNAR's AI companion — your cosmic guide through knowledge. Ask me anything about your studies, habits, or goals!",
    "study":      "The most effective study technique is the **Pomodoro method** — 25 minutes of deep focus, then a 5-minute rest. Use LUNAR's Study Planner to track your sessions!",
    "habit":      "Habits are the invisible architecture of your daily life. Start with **2-minute habits** — tiny actions that anchor larger behaviours. Track them in LUNAR's Habit Tracker!",
    "motivation": "Remember why you started. The universe is 13.8 billion years old — your setback is temporary. You are made of the same stardust as the greatest minds in history. ✨",
    "focus":      "To enter deep focus: close unnecessary tabs, put your phone on Do Not Disturb, and use the LUNAR Pomodoro timer. Your brain enters flow state after ~15 minutes of sustained attention.",
    "notes":      "The best notes are **active, not passive**. Instead of copying text, write in your own words. Try the Cornell Notes method — LUNAR's Notes page is perfect for it!",
    "journal":    "Daily journalling rewires your brain for clarity. Even 5 sentences about what you learned today creates compounding reflection over time.",
    "xp":         "XP (Experience Points) is earned by completing quests, logging habits, writing journal entries, and adding to your library. Level up to unlock new titles!",
    "level":      "You progress through levels from Stargazer all the way to LUNAR Master. Each level represents real growth — tracked through your XP earned.",
    "quest":      "Quests are daily and weekly challenges that reward XP. Complete them to level up and unlock achievements. Check your Quest System page!",
}


def generate_ai_response(user_message: str) -> str:
    """Generate a contextual AI response. Placeholder for OpenAI integration."""
    msg_lower = user_message.lower()

    # Check for keyword matches
    for keyword, response in AI_RESPONSES.items():
        if keyword in msg_lower:
            return response

    # Fallback: wisdom + suggestion
    quote = random.choice(WISDOM_QUOTES)
    follow_ups = [
        "Would you like tips on studying more effectively?",
        "I can help you build better habits or set up a study plan.",
        "Ask me about productivity, focus techniques, or how to use LUNAR's features.",
        "Try asking about study tips, habit building, or motivation!",
    ]
    return f"{quote}\n\n*{random.choice(follow_ups)}*"


# NOTE: To enable real OpenAI responses, replace `generate_ai_response` with:
#
# import openai
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# def generate_ai_response(user_message: str) -> str:
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are LUNAR's AI assistant — wise, encouraging, and knowledgeable about learning and productivity."},
#             {"role": "user",   "content": user_message}
#         ]
#     )
#     return response.choices[0].message.content
