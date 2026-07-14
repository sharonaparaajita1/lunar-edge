"""
LUNAR — Habit Tracker
Track habits with 7-day grid and progress charts.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import date, timedelta
from styles.theme import inject_theme
from database import (get_habits, create_habit, delete_habit,
                      toggle_habit_completion, get_habit_completions,
                      update_user_xp, check_and_unlock_achievements, init_db)
from utils.helpers import require_login, refresh_user, empty_state, last_n_days, today_str, HABIT_COLORS, toast_xp
from config import XP_PER_HABIT

st.set_page_config(page_title="Habit Tracker · LUNAR", page_icon="⚡", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>⚡ Habit Tracker</h1>
    <p style="color:#94a3b8; margin:0;">Small habits. Cosmic results.</p>
</div><hr>
""", unsafe_allow_html=True)

col_add, col_main = st.columns([1, 3])

with col_add:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:1rem;">✦ New Habit</h4>', unsafe_allow_html=True)
    with st.form("add_habit", clear_on_submit=True):
        h_name  = st.text_input("Habit name *", placeholder="Read for 20 minutes")
        h_color = st.selectbox("Colour", HABIT_COLORS,
                                format_func=lambda c: f"● {c}")
        if st.form_submit_button("✦ Add Habit", use_container_width=True):
            if not h_name.strip():
                st.error("Habit name required.")
            else:
                create_habit(user["id"], h_name.strip(), h_color)
                check_and_unlock_achievements(user["id"])
                refresh_user()
                st.toast("Habit created! ✦", icon="⚡")
                st.rerun()

    st.markdown("---")
    st.markdown("""
    <div class="lunar-card">
        <p style="color:#a78bfa; font-size:0.8rem; font-weight:600; margin-bottom:0.5rem;">✦ Tips</p>
        <ul style="color:#64748b; font-size:0.78rem; line-height:1.9; padding-left:1.1rem; margin:0;">
            <li>Start with 2–3 habits</li>
            <li>Stack habits together</li>
            <li>Never miss twice</li>
            <li>Each check-in = XP</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_main:
    habits      = get_habits(user["id"])
    completions = get_habit_completions(user["id"])
    days        = last_n_days(7)

    if not habits:
        empty_state("⚡", "No Habits Yet", "Build your first habit to start tracking. Small steps, celestial results.")
    else:
        # Stats
        today_done  = sum(1 for h in habits if today_str() in completions.get(h["id"], []))
        total_compl = sum(len(v) for v in completions.values())
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(habits)}</div><div class="metric-label">Active Habits</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{today_done}/{len(habits)}</div><div class="metric-label">Done Today</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total_compl}</div><div class="metric-label">All-Time Check-ins</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 7-day grid header
        day_labels = [(date.fromisoformat(d)).strftime("%a\n%d") for d in days]
        header_html = '<div style="display:grid; grid-template-columns:180px ' + ' '.join(['50px'] * 7) + ' 80px 60px; gap:6px; align-items:center; margin-bottom:0.5rem;">'
        header_html += '<div style="color:#64748b; font-size:0.7rem;">Habit</div>'
        for d, lbl in zip(days, day_labels):
            is_today = (d == today_str())
            color = "#a78bfa" if is_today else "#475569"
            header_html += f'<div style="text-align:center; font-size:0.65rem; color:{color}; white-space:pre-line;">{lbl}</div>'
        header_html += '<div style="text-align:center; color:#64748b; font-size:0.7rem;">Streak</div>'
        header_html += '<div></div>'
        header_html += '</div>'
        st.markdown(header_html, unsafe_allow_html=True)

        for habit in habits:
            h_id     = habit["id"]
            h_done   = completions.get(h_id, [])
            color    = habit.get("color", "#7c3aed")

            # Calculate streak
            streak = 0
            check  = date.today()
            while check.isoformat() in h_done:
                streak += 1
                check  = check - timedelta(days=1)

            row_html = '<div style="display:grid; grid-template-columns:180px ' + ' '.join(['50px'] * 7) + ' 80px 60px; gap:6px; align-items:center; margin-bottom:6px;">'
            row_html += f'<div style="color:#e2e8f0; font-size:0.85rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="{habit["name"]}">{habit["name"]}</div>'
            for d in days:
                done = d in h_done
                dot_style = f"background:{color}; box-shadow:0 0 8px {color};" if done else "background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);"
                row_html += f'<div style="display:flex; justify-content:center;"><div style="width:22px;height:22px;border-radius:50%;{dot_style};"></div></div>'
            row_html += f'<div style="text-align:center; color:{color}; font-weight:700; font-size:0.9rem;">{streak}🔥</div>'
            row_html += '</div>'
            st.markdown(row_html, unsafe_allow_html=True)

            # Today's check-in button + delete
            btn_c1, btn_c2, spacer = st.columns([1, 1, 6])
            today_done_h = today_str() in h_done
            with btn_c1:
                btn_label = "✓ Done" if today_done_h else "Mark Done"
                btn_style = "background:rgba(34,197,94,0.2);" if today_done_h else ""
                if st.button(btn_label, key=f"hc_{h_id}", use_container_width=True):
                    newly = toggle_habit_completion(h_id, user["id"], today_str())
                    if newly:
                        update_user_xp(user["id"], XP_PER_HABIT)
                        check_and_unlock_achievements(user["id"])
                        refresh_user()
                        toast_xp(XP_PER_HABIT, habit["name"])
                    st.rerun()
            with btn_c2:
                if st.button("🗑", key=f"del_h_{h_id}"):
                    delete_habit(h_id)
                    st.rerun()

            st.markdown("<div style='margin-bottom:0.4rem;'></div>", unsafe_allow_html=True)

        # Completion chart
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1.1rem;">📊 7-Day Overview</h3>', unsafe_allow_html=True)

        chart_days = last_n_days(7)
        y_vals = [sum(1 for h in habits if d in completions.get(h["id"], [])) for d in chart_days]
        x_labels = [(date.fromisoformat(d)).strftime("%a %d") for d in chart_days]

        fig = go.Figure(go.Bar(
            x=x_labels, y=y_vals,
            marker=dict(color=[f"rgba(124,58,237,{0.4 + 0.6 * (v / max(y_vals, default=1))})" for v in y_vals],
                        line=dict(color="#7c3aed", width=1)),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickformat="d"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            height=220,
        )
        st.plotly_chart(fig, use_container_width=True)
