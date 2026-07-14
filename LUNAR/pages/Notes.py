"""
LUNAR — Notes
Rich notes with folders, search, and pin.
"""

import streamlit as st
from styles.theme import inject_theme
from database import (get_notes, get_note_folders, create_note,
                      update_note, delete_note, init_db)
from utils.helpers import require_login, empty_state, format_date

st.set_page_config(page_title="Notes · LUNAR", page_icon="📝", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>📝 Notes</h1>
    <p style="color:#94a3b8; margin:0;">Capture your thoughts. Organise your mind.</p>
</div><hr>
""", unsafe_allow_html=True)

col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:1rem;">📁 Folders</h4>', unsafe_allow_html=True)

    folders = get_note_folders(user["id"])
    selected_folder = st.radio("Folder", folders, label_visibility="collapsed")

    st.markdown("---")
    search = st.text_input("🔍 Search", placeholder="Search notes...")

    st.markdown("---")
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:0.5rem;">✦ New Note</h4>', unsafe_allow_html=True)

    with st.form("new_note", clear_on_submit=True):
        n_title   = st.text_input("Title *", placeholder="My Note")
        n_folder  = st.text_input("Folder",  placeholder="General", value="General")
        n_content = st.text_area("Content", placeholder="Write your thoughts...", height=120)
        n_pin     = st.checkbox("📌 Pin this note")
        if st.form_submit_button("✦ Save Note", use_container_width=True):
            if not n_title.strip():
                st.error("Title is required.")
            else:
                note = create_note(user["id"], n_title.strip(), n_content, n_folder.strip() or "General")
                if n_pin:
                    update_note(note["id"], pinned=1)
                st.toast("Note saved! ✦", icon="📝")
                st.rerun()

with col_main:
    notes = get_notes(user["id"], folder=selected_folder, search=search)
    total = len(get_notes(user["id"]))
    pinned_count = sum(1 for n in get_notes(user["id"]) if n["pinned"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Notes</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{pinned_count}</div><div class="metric-label">Pinned</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not notes:
        empty_state("📝", "No Notes Here", "Start capturing your celestial thoughts — every great mind began with a blank page.")
    else:
        # Separate pinned
        pinned = [n for n in notes if n["pinned"]]
        others = [n for n in notes if not n["pinned"]]

        def render_notes_grid(note_list: list) -> None:
            cols = st.columns(2)
            for i, note in enumerate(note_list):
                with cols[i % 2]:
                    pin_icon = "📌 " if note["pinned"] else ""
                    preview = note["content"][:120] + "..." if len(note["content"]) > 120 else note["content"]

                    with st.expander(f"{pin_icon}{note['title']}", expanded=False):
                        st.markdown(f"""
                        <div style="color:#94a3b8; font-size:0.75rem; margin-bottom:0.8rem;">
                            📁 {note['folder']} · {format_date(note['updated_at'][:10])}
                        </div>
                        <div style="color:#e2e8f0; font-size:0.9rem; line-height:1.6; white-space:pre-wrap;">{note['content'] or '*No content yet*'}</div>
                        """, unsafe_allow_html=True)

                        edit_content = st.text_area("Edit", value=note["content"], height=100, key=f"edit_{note['id']}", label_visibility="collapsed")
                        ec1, ec2, ec3 = st.columns(3)
                        with ec1:
                            if st.button("💾 Save", key=f"save_{note['id']}", use_container_width=True):
                                update_note(note["id"], content=edit_content)
                                st.toast("Note updated!", icon="💾")
                                st.rerun()
                        with ec2:
                            pin_lbl = "📌 Unpin" if note["pinned"] else "📌 Pin"
                            if st.button(pin_lbl, key=f"pin_{note['id']}", use_container_width=True):
                                update_note(note["id"], pinned=0 if note["pinned"] else 1)
                                st.rerun()
                        with ec3:
                            if st.button("🗑 Delete", key=f"del_{note['id']}", use_container_width=True):
                                delete_note(note["id"])
                                st.toast("Note deleted.", icon="🗑️")
                                st.rerun()

        if pinned:
            st.markdown('<p style="color:#fde68a; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;">📌 Pinned</p>', unsafe_allow_html=True)
            render_notes_grid(pinned)
            st.markdown("<br>", unsafe_allow_html=True)
        if others:
            if pinned:
                st.markdown('<p style="color:#64748b; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;">All Notes</p>', unsafe_allow_html=True)
            render_notes_grid(others)
