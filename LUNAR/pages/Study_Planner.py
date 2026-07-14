"""
LUNAR — Study Planner
Tasks, subjects, deadlines, Pomodoro timer.
"""

import streamlit as st
import time
from styles.theme import inject_theme
from database import (get_tasks, create_task, toggle_task, delete_task,
                      update_user_xp, check_and_unlock_achievements, init_db)
from utils.helpers import (require_login, refresh_user, empty_state,
                           format_date, priority_badge_html, SUBJECT_COLORS, PRIORITY_COLORS)
from config import TASK_PRIORITIES, TASK_SUBJECTS, XP_PER_TASK

st.set_page_config(page_title="Study Planner · LUNAR", page_icon="📅", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>📅 Study Planner</h1>
    <p style="color:#94a3b8; margin:0;">Command your time. Conquer your subjects.</p>
</div><hr>
""", unsafe_allow_html=True)

tab_tasks, tab_pomodoro = st.tabs(["📋  Tasks", "⏱️  Pomodoro Timer"])

# ── TASKS ───────────────────────────────────────────────────────
with tab_tasks:
    col_add, col_list = st.columns([1, 2])

    with col_add:
        st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:1rem;">✦ Add Task</h4>', unsafe_allow_html=True)
        with st.form("add_task", clear_on_submit=True):
            new_title    = st.text_input("Task *", placeholder="Complete Chapter 5")
            new_subject  = st.selectbox("Subject", TASK_SUBJECTS)
            new_deadline = st.date_input("Deadline")
            new_priority = st.selectbox("Priority", TASK_PRIORITIES)
            add_btn      = st.form_submit_button("✦ Add Task", use_container_width=True)

            if add_btn:
                if not new_title.strip():
                    st.error("Task title is required.")
                else:
                    create_task(user["id"], new_title.strip(), new_subject,
                                str(new_deadline), new_priority)
                    st.toast("Task added! ✦", icon="📅")
                    st.rerun()

        # Filter
        st.markdown("---")
        st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.5rem;">Filter</h4>', unsafe_allow_html=True)
        show_completed = st.checkbox("Show completed", value=True)
        priority_filter = st.multiselect("Priority", TASK_PRIORITIES, default=TASK_PRIORITIES)
        subject_filter  = st.multiselect("Subject",  TASK_SUBJECTS,  default=[])

    with col_list:
        tasks = get_tasks(user["id"])

        # Apply filters
        if not show_completed:
            tasks = [t for t in tasks if not t["completed"]]
        if priority_filter:
            tasks = [t for t in tasks if t["priority"] in priority_filter]
        if subject_filter:
            tasks = [t for t in tasks if t["subject"] in subject_filter]

        # Stats
        all_tasks = get_tasks(user["id"])
        total = len(all_tasks)
        done  = sum(1 for t in all_tasks if t["completed"])
        pct   = int(done / total * 100) if total else 0

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Tasks</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{done}</div><div class="metric-label">Completed</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pct}%</div><div class="metric-label">Progress</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if total:
            st.progress(pct / 100)

        st.markdown("<br>", unsafe_allow_html=True)

        if not tasks:
            empty_state("📅", "No Tasks Found", "Add your first study task to begin your celestial conquest.")
        else:
            for task in tasks:
                subj_color = SUBJECT_COLORS.get(task["subject"], "#94a3b8")
                done_style = "opacity:0.45; text-decoration:line-through;" if task["completed"] else ""
                cb_col, info_col, act_col = st.columns([0.5, 6, 1])

                with cb_col:
                    checked = st.checkbox("", value=bool(task["completed"]), key=f"chk_{task['id']}")
                    if checked != bool(task["completed"]):
                        newly_done = toggle_task(task["id"])
                        if newly_done:
                            update_user_xp(user["id"], XP_PER_TASK)
                            check_and_unlock_achievements(user["id"])
                            refresh_user()
                            st.toast(f"✨ +{XP_PER_TASK} XP — Task complete!", icon="⭐")
                        st.rerun()

                with info_col:
                    st.markdown(f"""
                    <div class="lunar-card" style="padding:0.8rem 1.2rem; {done_style}">
                        <div style="display:flex; gap:0.6rem; align-items:center; margin-bottom:0.3rem; flex-wrap:wrap;">
                            <span style="font-weight:600; color:#e2e8f0; font-size:0.9rem;">{task['title']}</span>
                            {priority_badge_html(task['priority'])}
                        </div>
                        <div style="display:flex; gap:1rem; color:#64748b; font-size:0.75rem;">
                            <span style="color:{subj_color};">◈ {task['subject']}</span>
                            {f"<span>Due: {format_date(task['deadline'])}</span>" if task['deadline'] else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with act_col:
                    if st.button("🗑", key=f"del_t_{task['id']}", help="Delete"):
                        delete_task(task["id"])
                        st.rerun()

# ── POMODORO ─────────────────────────────────────────────────────
with tab_pomodoro:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 2rem;">
        <h2 style="font-family:'Cinzel',serif; color:#a78bfa; margin-bottom:0.5rem;">⏱️ Pomodoro Timer</h2>
        <p style="color:#64748b; font-size:0.9rem;">25 minutes of deep focus. 5 minutes of rest. Repeat.</p>
    </div>
    """, unsafe_allow_html=True)

    WORK_S  = 25 * 60
    BREAK_S =  5 * 60

    # Initialise session state
    if "pomo_running"    not in st.session_state: st.session_state.pomo_running    = False
    if "pomo_seconds"    not in st.session_state: st.session_state.pomo_seconds    = WORK_S
    if "pomo_mode"       not in st.session_state: st.session_state.pomo_mode       = "work"
    if "pomo_sessions"   not in st.session_state: st.session_state.pomo_sessions   = 0
    if "pomo_last_tick"  not in st.session_state: st.session_state.pomo_last_tick  = None

    # Tick logic
    if st.session_state.pomo_running and st.session_state.pomo_last_tick:
        elapsed = time.time() - st.session_state.pomo_last_tick
        st.session_state.pomo_seconds = max(0, st.session_state.pomo_seconds - int(elapsed))
        st.session_state.pomo_last_tick = time.time()

        if st.session_state.pomo_seconds == 0:
            if st.session_state.pomo_mode == "work":
                st.session_state.pomo_sessions += 1
                update_user_xp(user["id"], 30)
                refresh_user()
                st.toast("🍅 Pomodoro complete! +30 XP. Take a break!", icon="⭐")
                st.session_state.pomo_mode    = "break"
                st.session_state.pomo_seconds = BREAK_S
            else:
                st.session_state.pomo_mode    = "work"
                st.session_state.pomo_seconds = WORK_S
                st.toast("☕ Break over! Time to focus.", icon="🌙")
            st.session_state.pomo_running = False

    secs   = st.session_state.pomo_seconds
    mins_d = secs // 60
    secs_d = secs % 60
    total  = WORK_S if st.session_state.pomo_mode == "work" else BREAK_S
    pct    = 1 - secs / total
    is_work = st.session_state.pomo_mode == "work"
    ring_color = "#7c3aed" if is_work else "#22c55e"

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Circular ring via SVG
        radius = 90
        circumference = 2 * 3.14159 * radius
        dash_offset = circumference * (1 - pct)
        mode_label = "🔮 FOCUS" if is_work else "☕ BREAK"
        mode_color = "#a78bfa" if is_work else "#86efac"

        st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; gap:1.5rem;">
            <div style="position:relative; width:220px; height:220px;">
                <svg width="220" height="220" viewBox="0 0 220 220" style="transform:rotate(-90deg);">
                    <circle cx="110" cy="110" r="{radius}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="12"/>
                    <circle cx="110" cy="110" r="{radius}" fill="none" stroke="{ring_color}"
                            stroke-width="12" stroke-dasharray="{circumference:.1f}"
                            stroke-dashoffset="{dash_offset:.1f}" stroke-linecap="round"
                            style="filter:drop-shadow(0 0 10px {ring_color});"/>
                </svg>
                <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center;">
                    <div style="font-family:'Cinzel',serif; font-size:2.8rem; font-weight:700;
                                color:#f1f5f9; line-height:1;">{mins_d:02d}:{secs_d:02d}</div>
                    <div style="color:{mode_color}; font-size:0.75rem; letter-spacing:0.15em; margin-top:0.3rem;">{mode_label}</div>
                </div>
            </div>

            <div style="color:#64748b; font-size:0.85rem; text-align:center;">
                Sessions completed today: <span style="color:#a78bfa; font-weight:600;">{st.session_state.pomo_sessions}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("▶ Start" if not st.session_state.pomo_running else "⏸ Pause", use_container_width=True):
                st.session_state.pomo_running = not st.session_state.pomo_running
                if st.session_state.pomo_running:
                    st.session_state.pomo_last_tick = time.time()
                st.rerun()
        with btn_c2:
            if st.button("↺ Reset", use_container_width=True):
                st.session_state.pomo_running = False
                st.session_state.pomo_seconds = WORK_S if is_work else BREAK_S
                st.session_state.pomo_last_tick = None
                st.rerun()
        with btn_c3:
            if st.button("⏭ Skip", use_container_width=True):
                st.session_state.pomo_running = False
                st.session_state.pomo_mode    = "break" if is_work else "work"
                st.session_state.pomo_seconds = BREAK_S if is_work else WORK_S
                st.session_state.pomo_last_tick = None
                st.rerun()

        if st.session_state.pomo_running:
            time.sleep(1)
            st.rerun()
