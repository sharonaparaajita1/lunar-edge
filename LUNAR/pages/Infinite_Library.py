"""
LUNAR — Infinite Library
Store and search books, articles, and notes.
"""

import streamlit as st
from styles.theme import inject_theme
from database import (get_library_items, create_library_item, toggle_bookmark,
                      delete_library_item, update_user_xp, check_and_unlock_achievements, init_db)
from utils.helpers import require_login, refresh_user, empty_state, format_date, toast_xp
from config import LIBRARY_CATEGORIES, XP_PER_LIBRARY_ITEM

st.set_page_config(page_title="Library · LUNAR", page_icon="📚", layout="wide")
init_db()
inject_theme()

user = require_login()

st.markdown("""
<div style="padding:0.5rem 0 1.5rem;">
    <h1>📚 Infinite Library</h1>
    <p style="color:#94a3b8; margin:0;">A universe of knowledge at your fingertips.</p>
</div><hr>
""", unsafe_allow_html=True)

# ── Sidebar controls ────────────────────────────────────────────
col_controls, col_main = st.columns([1, 3])

with col_controls:
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:1rem;">🔍 Search & Filter</h4>', unsafe_allow_html=True)
    search = st.text_input("Search", placeholder="Search titles, content...", label_visibility="collapsed")
    category_filter = st.selectbox("Category", LIBRARY_CATEGORIES)
    type_filter = st.selectbox("Type", ["All", "Book", "Article", "Note", "Research", "Inspiration"])

    st.markdown("---")
    st.markdown('<h4 style="font-family:\'Cinzel\',serif; color:#a78bfa; font-size:1rem; margin-bottom:1rem;">✦ Add Item</h4>', unsafe_allow_html=True)

    with st.form("add_library", clear_on_submit=True):
        new_title    = st.text_input("Title *", placeholder="The Art of Learning")
        new_type     = st.selectbox("Type", ["Book", "Article", "Note", "Research", "Inspiration"])
        new_category = st.selectbox("Category", [c for c in LIBRARY_CATEGORIES if c != "All"])
        new_content  = st.text_area("Description / Notes", placeholder="Key insights, summary, or content...", height=100)
        add_btn = st.form_submit_button("✦ Add to Library", use_container_width=True)

        if add_btn:
            if not new_title.strip():
                st.error("Title is required.")
            else:
                create_library_item(user["id"], new_title.strip(), new_type, new_category, new_content)
                update_user_xp(user["id"], XP_PER_LIBRARY_ITEM)
                check_and_unlock_achievements(user["id"])
                refresh_user()
                toast_xp(XP_PER_LIBRARY_ITEM, "Library item added")
                st.rerun()

with col_main:
    # Filter params
    cat = "" if category_filter == "All" else category_filter
    typ = "" if type_filter == "All" else type_filter
    items = get_library_items(user["id"], category=cat, item_type=typ, search=search)

    # Stats row
    total     = len(get_library_items(user["id"]))
    bookmarked = sum(1 for i in get_library_items(user["id"]) if i["bookmarked"])
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Items</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{bookmarked}</div><div class="metric-label">Bookmarked</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(items)}</div><div class="metric-label">Showing</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not items:
        empty_state("📚", "Your Library Awaits", "Add your first book, article, or note to begin building your collection of wisdom.")
    else:
        # 3-column grid
        TYPE_ICONS = {"Book": "📖", "Article": "📰", "Note": "📝", "Research": "🔬", "Inspiration": "✨"}
        TYPE_COLORS = {"Book": "purple", "Article": "blue", "Note": "green", "Research": "gold", "Inspiration": "purple"}

        cols = st.columns(3)
        for idx, item in enumerate(items):
            with cols[idx % 3]:
                icon  = TYPE_ICONS.get(item["item_type"], "📄")
                color = TYPE_COLORS.get(item["item_type"], "purple")
                bm    = "🔖" if item["bookmarked"] else "☆"

                st.markdown(f"""
                <div class="lunar-card" style="min-height:160px; position:relative;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.6rem;">
                        <span style="font-size:1.5rem;">{icon}</span>
                        <span class="lunar-badge badge-{color}">{item['item_type']}</span>
                    </div>
                    <div style="font-weight:600; color:#e2e8f0; font-size:0.9rem; margin-bottom:0.3rem; line-height:1.4;">
                        {item['title']}
                    </div>
                    <div style="color:#64748b; font-size:0.75rem; margin-bottom:0.5rem;">{item['category']}</div>
                    {f'<div style="color:#94a3b8; font-size:0.78rem; line-height:1.4; margin-bottom:0.5rem;">{item["content"][:100]}{"..." if len(item["content"]) > 100 else ""}</div>' if item['content'] else ''}
                    <div style="color:#475569; font-size:0.7rem; margin-top:auto;">{format_date(item['created_at'][:10])}</div>
                </div>
                """, unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(bm, key=f"bm_{item['id']}", help="Bookmark", use_container_width=True):
                        toggle_bookmark(item["id"])
                        st.rerun()
                with btn_col2:
                    if st.button("🗑", key=f"del_{item['id']}", help="Delete", use_container_width=True):
                        delete_library_item(item["id"])
                        st.toast("Item removed from library.", icon="🗑️")
                        st.rerun()
