"""
LUNAR — Premium AI Productivity Platform
Entry point. Run with: streamlit run app.py
"""

import streamlit as st
from styles.theme import inject_theme
from database import init_db

# ── Page config (must be first Streamlit call) ──────────────────
st.set_page_config(
    page_title="LUNAR",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": "LUNAR v1.0 — Your celestial productivity sanctuary."}
)

# ── Initialise database on first run ────────────────────────────
init_db()

# ── Inject global theme ─────────────────────────────────────────
inject_theme()

# ── Sidebar navigation ──────────────────────────────────────────
from utils.helpers import get_user, logout, xp_bar, refresh_user

user = get_user()

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size:2.5rem;">🌙</div>
        <h2 style="font-family:'Cinzel',serif; background:linear-gradient(135deg,#a78bfa,#60a5fa,#fde68a);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   background-clip:text; margin:0.3rem 0; font-size:1.8rem;">LUNAR</h2>
        <p style="color:#64748b; font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; margin:0;">
            Your Celestial Sanctuary
        </p>
    </div>
    <hr style="border-color:rgba(124,58,237,0.2);">
    """, unsafe_allow_html=True)

    if user:
        # User info
        st.markdown(f"""
        <div style="padding:0.8rem; background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.2);
                    border-radius:12px; margin-bottom:1rem;">
            <div style="display:flex; align-items:center; gap:0.8rem;">
                <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg,{user.get('avatar_color','#7c3aed')},{user.get('accent_color','#4f46e5')});
                            display:flex; align-items:center; justify-content:center; font-weight:700; font-size:1rem; flex-shrink:0;">
                    {user['username'][0].upper()}
                </div>
                <div>
                    <div style="font-weight:600; color:#f1f5f9; font-size:0.9rem;">{user['username']}</div>
                    <div style="color:#94a3b8; font-size:0.72rem;">{user.get('streak',0)} day streak 🔥</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        xp_bar(user.get("xp", 0))
        st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)

        # Navigation sections
        def nav_header(title: str):
            st.markdown(f"""
            <div style="color:#64748b; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.15em;
                        padding: 0.3rem 0; margin-top:0.5rem;">{title}</div>
            """, unsafe_allow_html=True)

        nav_header("Main")
        st.page_link("app.py",                       label="🏠  Dashboard",        )
        st.page_link("pages/AI_Assistant.py",         label="🤖  AI Assistant",     )

        nav_header("Learn")
        st.page_link("pages/Infinite_Library.py",     label="📚  Infinite Library", )
        st.page_link("pages/Study_Planner.py",        label="📅  Study Planner",    )
        st.page_link("pages/Notes.py",                label="📝  Notes",            )
        st.page_link("pages/Journal.py",              label="✍️  Journal",          )

        nav_header("Growth")
        st.page_link("pages/Habit_Tracker.py",        label="⚡  Habit Tracker",    )
        st.page_link("pages/Quest_System.py",         label="⚔️  Quests",           )
        st.page_link("pages/Achievements.py",         label="🏆  Achievements",     )

        nav_header("Insights")
        st.page_link("pages/Analytics.py",            label="📊  Analytics",        )
        st.page_link("pages/Profile.py",              label="👤  Profile",          )
        st.page_link("pages/Settings.py",             label="⚙️  Settings",         )

        st.markdown("<hr style='border-color:rgba(124,58,237,0.15); margin-top:1rem;'>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    else:
        st.page_link("pages/Login.py", label="🔑  Login / Sign Up")
        st.markdown("""
        <div style="text-align:center; padding:2rem 0; color:#64748b; font-size:0.8rem;">
            Your celestial journey<br>awaits beyond the gate.
        </div>
        """, unsafe_allow_html=True)

# ── Main page content (Dashboard if logged in, else landing) ────
if not user:
    # ── Landing page ─────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:4rem 2rem 2rem; min-height:70vh;
                display:flex; flex-direction:column; align-items:center; justify-content:center;">

        <div style="font-size:5rem; margin-bottom:1rem; animation:float 6s ease-in-out infinite;">🌙</div>

        <h1 style="font-size:4rem; margin-bottom:0.5rem; font-family:'Cinzel',serif;
                   background:linear-gradient(135deg,#a78bfa 0%,#60a5fa 50%,#fde68a 100%);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
                   filter:drop-shadow(0 0 30px rgba(167,139,250,0.4));">
            LUNAR
        </h1>

        <p style="font-size:1.3rem; color:#94a3b8; max-width:600px; line-height:1.8; margin-bottom:0.5rem;">
            Your <span style="color:#a78bfa;">celestial sanctuary</span> for learning,
            growth, and self-discovery.
        </p>
        <p style="color:#64748b; max-width:500px; line-height:1.7; margin-bottom:3rem; font-size:0.95rem;">
            Track habits. Complete quests. Collect wisdom. Level up your mind.
            LUNAR transforms your daily journey into an enchanted adventure.
        </p>
    </div>

    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(-5deg); }
            50%       { transform: translateY(-20px) rotate(5deg); }
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.page_link("pages/Login.py", label="✨  Enter LUNAR")

    # Feature highlights
    st.markdown("<br><br>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🤖", "AI Assistant", "Chat with your cosmic AI companion for study guidance"),
        ("⚔️", "Quest System", "Complete daily and weekly quests to earn XP and level up"),
        ("📚", "Infinite Library", "Store and search your knowledge across books and notes"),
        ("📊", "Analytics", "Visualise your growth with beautiful celestial charts"),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="lunar-card" style="text-align:center; min-height:160px;">
                <div style="font-size:2rem; margin-bottom:0.8rem;">{icon}</div>
                <h4 style="font-family:'Cinzel',serif; color:#a78bfa; margin-bottom:0.4rem; font-size:0.95rem;">{title}</h4>
                <p style="color:#64748b; font-size:0.8rem; line-height:1.5; margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

else:
    # ── Dashboard (redirected here when logged in) ──────────────
    from datetime import date
    import database as db
    from config import get_level_title, MOODS, MOOD_LABELS
    from utils.helpers import empty_state, format_date, today_str

    # Check/unlock achievements silently
    new_ach = db.check_and_unlock_achievements(user["id"])
    if new_ach:
        refresh_user()
        user = get_user()
        for aid in new_ach:
            st.toast(f"🏆 Achievement unlocked!", icon="🌟")

    # Seed quests if not already done
    db.seed_quests(user["id"])

    st.markdown(f"""
    <div style="padding:0.5rem 0 1.5rem;">
        <p style="color:#94a3b8; margin:0; font-size:0.9rem;">
            {date.today().strftime("%A, %B %d, %Y")}
        </p>
        <h1 style="font-size:2.4rem; margin:0.2rem 0 0.1rem;">
            Good evening, {user['username']} 🌙
        </h1>
        <p style="color:#64748b; margin:0; font-size:0.95rem;">
            Your celestial journey continues. What shall we conquer today?
        </p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # ── XP / Level row ─────────────────────────────────────────
    xp = user.get("xp", 0)
    level, title_lbl, xp_floor, xp_ceil = get_level_title(xp)
    streak = user.get("streak", 0)
    analytics = db.get_analytics(user["id"])

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{xp:,}</div>
            <div class="metric-label">Total XP</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Lv.{level}</div>
            <div class="metric-label">{title_lbl}</div>
        </div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{streak}🔥</div>
            <div class="metric-label">Day Streak</div>
        </div>""", unsafe_allow_html=True)
    with col_d:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{analytics['completed_tasks']}</div>
            <div class="metric-label">Tasks Done</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main content cols ───────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Today's Quests
        st.markdown("""<h3 style="font-family:'Cinzel',serif; color:#a78bfa; font-size:1.2rem;">
            ⚔️ Today's Quests</h3>""", unsafe_allow_html=True)

        daily_quests = db.get_quests(user["id"], "daily")
        if daily_quests:
            for q in daily_quests:
                c1, c2 = st.columns([5, 1])
                with c1:
                    done = bool(q["completed"])
                    style = "opacity:0.4; text-decoration:line-through;" if done else ""
                    st.markdown(f"""
                    <div class="lunar-card" style="padding:0.8rem 1.2rem; {style}">
                        <span style="color:#fde68a;">✦</span>
                        <span style="margin-left:0.5rem;">{q['name']}</span>
                        <span style="float:right; color:#a78bfa; font-size:0.8rem; font-weight:600;">+{q['xp_reward']} XP</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if not done:
                        if st.button("✓", key=f"dq_{q['id']}"):
                            earned = db.complete_quest(q["id"], user["id"])
                            refresh_user()
                            st.toast(f"⭐ Quest complete! +{earned} XP", icon="🌟")
                            st.rerun()
        else:
            empty_state("⚔️", "No Quests Yet", "Head to the Quest System to get started!")

        st.markdown("<br>", unsafe_allow_html=True)

        # Recent notes
        st.markdown("""<h3 style="font-family:'Cinzel',serif; color:#a78bfa; font-size:1.2rem;">
            📝 Recent Notes</h3>""", unsafe_allow_html=True)
        notes = db.get_notes(user["id"])[:3]
        if notes:
            for note in notes:
                st.markdown(f"""
                <div class="lunar-card" style="padding:0.8rem 1.2rem;">
                    <div style="font-weight:600; color:#e2e8f0;">{note['title']}</div>
                    <div style="color:#64748b; font-size:0.78rem; margin-top:0.2rem;">
                        {note['folder']} · {format_date(note['updated_at'][:10])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("📝", "No Notes Yet", "Start capturing your thoughts!")

    with col_right:
        # Mood selector
        st.markdown("""<h3 style="font-family:'Cinzel',serif; color:#a78bfa; font-size:1.2rem;">
            💫 Today's Mood</h3>""", unsafe_allow_html=True)

        today_entry = db.get_journal_entry(user["id"], today_str())
        current_mood = today_entry["mood"] if today_entry else 2

        mood_cols = st.columns(5)
        for i, (emoji, label) in enumerate(zip(MOODS, MOOD_LABELS)):
            with mood_cols[i]:
                selected = (i == current_mood)
                border = "border:2px solid #7c3aed; background:rgba(124,58,237,0.2);" if selected else "border:1px solid rgba(255,255,255,0.1);"
                st.markdown(f"""
                <div style="text-align:center; {border} border-radius:10px; padding:0.5rem;
                            cursor:pointer; transition:all 0.2s;">
                    <div style="font-size:1.5rem;">{emoji}</div>
                    <div style="font-size:0.6rem; color:#94a3b8;">{label}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(emoji, key=f"mood_{i}", help=label):
                    content = today_entry["content"] if today_entry else ""
                    db.upsert_journal_entry(user["id"], today_str(), i, content)
                    st.toast(f"Mood updated: {label} {emoji}", icon="💫")
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Library stats
        st.markdown("""<h3 style="font-family:'Cinzel',serif; color:#a78bfa; font-size:1.2rem;">
            📚 Library Stats</h3>""", unsafe_allow_html=True)

        lib_items = db.get_library_items(user["id"])
        books    = sum(1 for i in lib_items if i["item_type"] == "Book")
        articles = sum(1 for i in lib_items if i["item_type"] == "Article")
        items_notes = sum(1 for i in lib_items if i["item_type"] == "Note")

        c1, c2, c3 = st.columns(3)
        for col, (val, lbl) in zip([c1, c2, c3], [(books, "Books"), (articles, "Articles"), (items_notes, "Notes")]):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="padding:0.8rem;">
                    <div class="metric-value" style="font-size:1.5rem;">{val}</div>
                    <div class="metric-label">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Weekly quest
        st.markdown("""<h3 style="font-family:'Cinzel',serif; color:#a78bfa; font-size:1.2rem;">
            🌟 Weekly Challenge</h3>""", unsafe_allow_html=True)
        weekly = db.get_quests(user["id"], "weekly")
        for q in weekly[:2]:
            done = bool(q["completed"])
            style = "opacity:0.4;" if done else ""
            st.markdown(f"""
            <div class="lunar-card" style="padding:0.7rem 1rem; {style}">
                <div style="font-size:0.85rem;">🗓️ {q['name']}</div>
                <div style="color:#f59e0b; font-size:0.75rem; margin-top:0.2rem;">+{q['xp_reward']} XP</div>
            </div>
            """, unsafe_allow_html=True)
