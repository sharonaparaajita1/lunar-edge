"""
LUNAR — Analytics
Charts for study hours, habit completion, XP, daily activity.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
from styles.theme import inject_theme
from database import get_analytics, get_habits, get_habit_completions, init_db
from utils.helpers import require_login, last_n_days, empty_state

st.set_page_config(page_title="Analytics · LUNAR", page_icon="📊", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>📊 Analytics</h1>
    <p style="color:#94a3b8; margin:0;">Visualise your celestial growth over time.</p>
</div><hr>
""", unsafe_allow_html=True)

data   = get_analytics(user["id"])
habits = get_habits(user["id"])
comps  = get_habit_completions(user["id"])
days7  = last_n_days(7)
days14 = last_n_days(14)

# ── Chart helpers ────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", size=11),
    margin=dict(l=20, r=20, t=30, b=20),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    xaxis=dict(gridcolor="rgba(0,0,0,0)"),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
)

# ── Summary metrics ──────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    (data["total_tasks"],     "Total Tasks"),
    (data["completed_tasks"], "Completed"),
    (data["total_library"],   "Library Items"),
    (data["total_journal"],   "Journal Entries"),
    (data["total_habits"],    "Active Habits"),
]
for col, (val, lbl) in zip([c1, c2, c3, c4, c5], metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: XP + Habit Completion ────────────────────────────────
col_xp, col_hab = st.columns(2)

with col_xp:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.8rem;">⭐ XP Over Last 7 Days</h4>', unsafe_allow_html=True)
    xp_by_date = data.get("xp_by_date", {})
    y_xp = [xp_by_date.get(d, 0) for d in days7]
    x_xp = [(date.fromisoformat(d)).strftime("%a %d") for d in days7]

    fig_xp = go.Figure(go.Bar(
        x=x_xp, y=y_xp,
        marker=dict(
            color=[f"rgba(167,139,250,{max(0.3, v/max(y_xp or [1]))})" for v in y_xp],
            line=dict(color="#a78bfa", width=1)
        ),
        hovertemplate="%{x}<br>+%{y} XP<extra></extra>",
    ))
    fig_xp.update_layout(**PLOT_LAYOUT, height=250,
                          yaxis_title="XP Earned")
    st.plotly_chart(fig_xp, use_container_width=True)

with col_hab:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.8rem;">⚡ Habit Completions (14 Days)</h4>', unsafe_allow_html=True)
    hab_by_date = data.get("habits_by_date", {})
    y_hab = [hab_by_date.get(d, 0) for d in days14]
    x_hab = [(date.fromisoformat(d)).strftime("%b %d") for d in days14]

    fig_hab = go.Figure(go.Scatter(
        x=x_hab, y=y_hab,
        mode="lines+markers",
        line=dict(color="#3b82f6", width=2.5),
        marker=dict(color="#93c5fd", size=7),
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.1)",
        hovertemplate="%{x}<br>%{y} habits<extra></extra>",
    ))
    fig_hab.update_layout(**PLOT_LAYOUT, height=250,
                           yaxis_title="Habits Done")
    st.plotly_chart(fig_hab, use_container_width=True)

# ── Row 2: Per-habit breakdown + task completion donut ──────────
col_per_habit, col_donut = st.columns(2)

with col_per_habit:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.8rem;">📈 Per-Habit (7 Days)</h4>', unsafe_allow_html=True)
    if not habits:
        empty_state("⚡", "No Habits", "Add habits to see per-habit analytics.")
    else:
        names = [h["name"] for h in habits]
        vals  = [sum(1 for d in days7 if d in comps.get(h["id"], [])) for h in habits]
        colors = [h.get("color", "#7c3aed") for h in habits]

        fig_ph = go.Figure(go.Bar(
            x=names, y=vals,
            marker=dict(color=colors),
            hovertemplate="%{x}<br>%{y}/7 days<extra></extra>",
        ))
        fig_ph.update_layout(**PLOT_LAYOUT, height=250,
                              yaxis_title="Days Completed")
        st.plotly_chart(fig_ph, use_container_width=True)

with col_donut:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.8rem;">✅ Task Completion</h4>', unsafe_allow_html=True)
    done_n   = data["completed_tasks"]
    undone_n = max(data["total_tasks"] - done_n, 0)
    if data["total_tasks"] == 0:
        empty_state("📋", "No Tasks", "Add tasks in the Study Planner.")
    else:
        fig_d = go.Figure(go.Pie(
            labels=["Completed", "Pending"],
            values=[done_n, undone_n],
            hole=0.55,
            marker=dict(colors=["#7c3aed", "rgba(255,255,255,0.08)"],
                        line=dict(color="#0a0a1a", width=2)),
            textfont=dict(color="#f1f5f9"),
            hovertemplate="%{label}: %{value}<extra></extra>",
        ))
        fig_d.update_layout(**PLOT_LAYOUT, height=250,
                             annotations=[dict(text=f"{done_n}<br>done", x=0.5, y=0.5,
                                               font_size=14, font_color="#a78bfa",
                                               showarrow=False)])
        st.plotly_chart(fig_d, use_container_width=True)

# ── Content breakdown ────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.8rem;">📚 Knowledge Library Breakdown</h4>', unsafe_allow_html=True)

from database import get_library_items
lib_items = get_library_items(user["id"])
type_counts: dict[str, int] = {}
for item in lib_items:
    t = item.get("item_type", "Other")
    type_counts[t] = type_counts.get(t, 0) + 1

if type_counts:
    fig_lib = go.Figure(go.Bar(
        x=list(type_counts.keys()),
        y=list(type_counts.values()),
        marker=dict(color=["#7c3aed", "#3b82f6", "#22c55e", "#f59e0b", "#ec4899"],
                    line=dict(color="#0a0a1a", width=1)),
        hovertemplate="%{x}: %{y} items<extra></extra>",
    ))
    fig_lib.update_layout(**PLOT_LAYOUT, height=220, yaxis_title="Count")
    st.plotly_chart(fig_lib, use_container_width=True)
else:
    empty_state("📚", "Library Empty", "Add items to see your collection breakdown.")
