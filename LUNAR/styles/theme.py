"""
LUNAR Global CSS Theme
Injects the magical dark fantasy styles into every Streamlit page.
"""

LUNAR_CSS = """
<style>
/* ── Google Fonts ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root variables ────────────────────────────────────────────── */
:root {
    --bg-dark:       #0a0a1a;
    --bg-card:       rgba(15, 15, 40, 0.85);
    --purple:        #7c3aed;
    --purple-light:  #a78bfa;
    --blue:          #3b82f6;
    --blue-light:    #93c5fd;
    --silver:        #e2e8f0;
    --gold:          #f59e0b;
    --gold-light:    #fde68a;
    --text-primary:  #f1f5f9;
    --text-muted:    #94a3b8;
    --glow-purple:   0 0 20px rgba(124,58,237,0.5), 0 0 40px rgba(124,58,237,0.2);
    --glow-blue:     0 0 20px rgba(59,130,246,0.5), 0 0 40px rgba(59,130,246,0.2);
    --glow-gold:     0 0 20px rgba(245,158,11,0.5), 0 0 40px rgba(245,158,11,0.2);
}

/* ── Page background ───────────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0f0a2e 30%, #0a1628 60%, #0a0a1a 100%);
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

/* Animated star particles */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 15%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 35%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 70%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 95% 10%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(2px 2px at 15% 45%, rgba(167,139,250,0.6) 0%, transparent 100%),
        radial-gradient(2px 2px at 60% 55%, rgba(147,197,253,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 25%, rgba(253,230,138,0.7) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
    animation: twinkle 8s ease-in-out infinite alternate;
}

@keyframes twinkle {
    0%   { opacity: 0.6; }
    50%  { opacity: 1.0; }
    100% { opacity: 0.7; }
}

/* ── Hide Streamlit chrome ─────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10,10,40,0.98) 0%, rgba(15,10,45,0.98) 100%);
    border-right: 1px solid rgba(124,58,237,0.3);
    box-shadow: 4px 0 30px rgba(124,58,237,0.1);
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Headings ────────────────────────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--text-primary) !important;
}
h1 {
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #fde68a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none !important;
    filter: drop-shadow(0 0 20px rgba(167,139,250,0.4));
}

/* ── Cards ───────────────────────────────────────────────────────── */
.lunar-card {
    background: rgba(15, 15, 45, 0.75);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 30px rgba(124,58,237,0.1), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: border-color 0.3s, box-shadow 0.3s;
    margin-bottom: 1rem;
}
.lunar-card:hover {
    border-color: rgba(124,58,237,0.5);
    box-shadow: 0 8px 40px rgba(124,58,237,0.2);
}

/* ── Metric cards ────────────────────────────────────────────────── */
.metric-card {
    background: rgba(15,15,45,0.8);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    backdrop-filter: blur(8px);
}
.metric-value {
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.25rem;
}

/* ── Buttons ─────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.5) !important;
    border-color: rgba(167,139,250,0.6) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Inputs ──────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(15,15,45,0.9) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(124,58,237,0.7) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label { color: var(--text-muted) !important; }

/* ── Progress bars ───────────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #a78bfa) !important;
    box-shadow: 0 0 10px rgba(124,58,237,0.5);
}
.stProgress > div > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 999px;
}

/* ── Tabs ────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,10,30,0.8);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: var(--text-muted) !important;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.4);
}

/* ── Checkboxes ──────────────────────────────────────────────────── */
.stCheckbox > label { color: var(--text-primary) !important; }

/* ── Selectbox dropdown ──────────────────────────────────────────── */
.stSelectbox > div > div { color: var(--text-primary) !important; }

/* ── Expander ────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(15,15,45,0.8) !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Scrollbar ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(10,10,30,0.5); }
::-webkit-scrollbar-thumb {
    background: rgba(124,58,237,0.5);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.8); }

/* ── Badge ───────────────────────────────────────────────────────── */
.lunar-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.badge-purple { background: rgba(124,58,237,0.2); color: #a78bfa; border: 1px solid rgba(124,58,237,0.4); }
.badge-gold   { background: rgba(245,158,11,0.2); color: #fde68a; border: 1px solid rgba(245,158,11,0.4); }
.badge-blue   { background: rgba(59,130,246,0.2); color: #93c5fd; border: 1px solid rgba(59,130,246,0.4); }
.badge-green  { background: rgba(34,197,94,0.2);  color: #86efac; border: 1px solid rgba(34,197,94,0.4); }
.badge-red    { background: rgba(239,68,68,0.2);  color: #fca5a5; border: 1px solid rgba(239,68,68,0.4); }

/* ── Chat bubbles ────────────────────────────────────────────────── */
.chat-user {
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(79,70,229,0.3));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
    color: var(--text-primary);
    font-size: 0.9rem;
}
.chat-ai {
    background: rgba(15,15,50,0.8);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 16px 16px 16px 4px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    max-width: 85%;
    color: var(--text-primary);
    font-size: 0.9rem;
    box-shadow: 0 0 20px rgba(59,130,246,0.1);
}

/* ── Achievement card ────────────────────────────────────────────── */
.ach-card-unlocked {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(245,158,11,0.1));
    border: 1px solid rgba(245,158,11,0.4);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 0 20px rgba(245,158,11,0.15);
}
.ach-card-locked {
    background: rgba(10,10,30,0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    opacity: 0.4;
    filter: grayscale(80%);
}
.ach-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.ach-name { font-family: 'Cinzel', serif; font-size: 0.9rem; color: #fde68a; }
.ach-desc { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem; }

/* ── Habit grid ──────────────────────────────────────────────────── */
.habit-dot {
    width: 20px; height: 20px;
    border-radius: 50%;
    display: inline-block;
}
.habit-dot-done { background: linear-gradient(135deg, #7c3aed, #a78bfa); box-shadow: 0 0 8px rgba(124,58,237,0.6); }
.habit-dot-miss { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); }

/* ── Divider ─────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(124,58,237,0.2) !important;
    margin: 1.5rem 0 !important;
}

/* ── Plotly chart background ─────────────────────────────────────── */
.js-plotly-plot .plotly .bg { fill: rgba(10,10,30,0) !important; }
</style>
"""


def inject_theme():
    """Call this at the top of every page to apply the LUNAR theme."""
    import streamlit as st
    st.markdown(LUNAR_CSS, unsafe_allow_html=True)


def card(content_html: str, extra_class: str = "") -> str:
    """Wrap HTML in a lunar-card div."""
    return f'<div class="lunar-card {extra_class}">{content_html}</div>'


def badge(text: str, color: str = "purple") -> str:
    return f'<span class="lunar-badge badge-{color}">{text}</span>'


def metric_card(value: str, label: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    import streamlit as st
    st.markdown(f"""
    <div style="padding: 1rem 0 0.5rem;">
        <h1 style="font-size:2.2rem; margin-bottom:0.2rem;">{icon} {title}</h1>
        {f'<p style="color:#94a3b8; margin:0; font-size:0.95rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    <hr>
    """, unsafe_allow_html=True)
