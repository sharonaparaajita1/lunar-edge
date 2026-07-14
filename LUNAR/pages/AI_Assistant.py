"""
LUNAR — AI Assistant
Modern chat interface with placeholder OpenAI integration.
"""

import streamlit as st
from styles.theme import inject_theme
from database import get_chat_history, add_chat_message, clear_chat_history, init_db, update_user_xp
from utils.helpers import require_login, generate_ai_response, refresh_user, format_datetime
from config import XP_PER_QUEST

st.set_page_config(page_title="AI Assistant · LUNAR", page_icon="🤖", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>🤖 AI Assistant</h1>
    <p style="color:#94a3b8; margin:0;">Your cosmic guide through knowledge and wisdom.</p>
</div><hr>
""", unsafe_allow_html=True)

col_chat, col_info = st.columns([3, 1])

with col_info:
    st.markdown("""
    <div class="lunar-card">
        <h4 style="font-family:'Cinzel',serif; color:#a78bfa; margin-bottom:1rem; font-size:0.95rem;">✦ Ask Me About</h4>
        <ul style="color:#94a3b8; font-size:0.82rem; line-height:2; padding-left:1.2rem; margin:0;">
            <li>Study techniques</li>
            <li>Habit building</li>
            <li>Motivation & mindset</li>
            <li>How to use LUNAR</li>
            <li>Memory & focus tips</li>
            <li>Note-taking methods</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lunar-card" style="margin-top:1rem;">
        <h4 style="font-family:'Cinzel',serif; color:#a78bfa; margin-bottom:0.5rem; font-size:0.95rem;">⚡ Quick Prompts</h4>
    </div>
    """, unsafe_allow_html=True)

    quick_prompts = [
        "Study techniques",
        "Help me focus",
        "Motivation boost",
        "Habit advice",
        "What is XP?",
    ]
    for prompt in quick_prompts:
        if st.button(prompt, key=f"qp_{prompt}", use_container_width=True):
            st.session_state["pending_prompt"] = prompt

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History", use_container_width=True):
        clear_chat_history(user["id"])
        st.rerun()

with col_chat:
    history = get_chat_history(user["id"], limit=60)

    # Render chat history
    chat_container = st.container()
    with chat_container:
        if not history:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; opacity:0.6;">
                <div style="font-size:3rem; margin-bottom:1rem;">🌙</div>
                <h3 style="color:#a78bfa; font-family:'Cinzel',serif;">LUNAR AI awaits</h3>
                <p style="color:#64748b; font-size:0.9rem;">
                    Greetings, celestial scholar. I am your AI companion,<br>
                    ready to illuminate the path of knowledge.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; margin:0.4rem 0;">
                        <div class="chat-user">
                            <div style="font-size:0.82rem; color:#94a3b8; margin-bottom:0.3rem;">You · {format_datetime(msg['created_at'])}</div>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    import re
                    content = msg["content"]
                    # Basic markdown: bold, italic, code
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
                    content = re.sub(r'`(.*?)`', r'<code style="background:rgba(124,58,237,0.2);padding:1px 4px;border-radius:4px;">\1</code>', content)
                    content = content.replace("\n", "<br>")
                    st.markdown(f"""
                    <div style="display:flex; margin:0.4rem 0; gap:0.8rem; align-items:flex-start;">
                        <div style="width:32px; height:32px; border-radius:50%; background:linear-gradient(135deg,#3b82f6,#7c3aed);
                                    display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:0.85rem; margin-top:0.3rem;">🤖</div>
                        <div class="chat-ai">
                            <div style="font-size:0.82rem; color:#64748b; margin-bottom:0.3rem;">LUNAR AI · {format_datetime(msg['created_at'])}</div>
                            {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Handle quick prompt
    pending = st.session_state.pop("pending_prompt", None)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Message",
            value=pending or "",
            placeholder="Ask LUNAR anything... study tips, motivation, how the app works...",
            height=80,
            label_visibility="collapsed"
        )
        send_col, hint_col = st.columns([1, 4])
        with send_col:
            submitted = st.form_submit_button("Send ✨", use_container_width=True)
        with hint_col:
            st.markdown('<p style="color:#475569; font-size:0.78rem; margin:0.6rem 0 0;">Shift+Enter for new line</p>', unsafe_allow_html=True)

    if submitted and user_input.strip():
        msg = user_input.strip()
        add_chat_message(user["id"], "user", msg)

        with st.spinner("🌙 Consulting the cosmic archives..."):
            response = generate_ai_response(msg)

        add_chat_message(user["id"], "assistant", response)

        # Award small XP for using assistant
        if len(get_chat_history(user["id"])) % 10 == 0:
            update_user_xp(user["id"], 5)
            refresh_user()
            st.toast("✨ +5 XP — Keep exploring!", icon="⭐")

        st.rerun()
