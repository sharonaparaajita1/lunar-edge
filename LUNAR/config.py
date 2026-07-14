"""
LUNAR Configuration
Central config for colors, constants, and app settings.
"""

APP_NAME = "LUNAR"
APP_VERSION = "1.0.0"
APP_ICON = "🌙"

# ── Colour palette ────────────────────────────────────────────────
COLORS = {
    "bg_dark":       "#0a0a1a",
    "bg_card":       "rgba(20,20,50,0.7)",
    "purple":        "#7c3aed",
    "purple_light":  "#a78bfa",
    "blue":          "#3b82f6",
    "blue_light":    "#93c5fd",
    "silver":        "#e2e8f0",
    "gold":          "#f59e0b",
    "gold_light":    "#fde68a",
    "text_primary":  "#f1f5f9",
    "text_muted":    "#94a3b8",
    "success":       "#22c55e",
    "danger":        "#ef4444",
    "warning":       "#f59e0b",
}

# ── XP / levelling ────────────────────────────────────────────────
XP_PER_QUEST        = 50
XP_PER_HABIT        = 10
XP_PER_JOURNAL      = 20
XP_PER_LIBRARY_ITEM = 15
XP_PER_TASK         = 25

LEVEL_TITLES = [
    (0,    "Stargazer"),
    (100,  "Moon Apprentice"),
    (300,  "Lunar Scholar"),
    (600,  "Celestial Sage"),
    (1000, "Astral Wizard"),
    (1500, "Cosmic Archon"),
    (2500, "Ethereal Oracle"),
    (4000, "LUNAR Master"),
]

def get_level_title(xp: int) -> tuple[int, str, int, int]:
    """Return (level_index, title, xp_for_current, xp_for_next)."""
    level = 0
    title = LEVEL_TITLES[0][1]
    xp_floor = 0
    for i, (threshold, lbl) in enumerate(LEVEL_TITLES):
        if xp >= threshold:
            level = i
            title = lbl
            xp_floor = threshold
        else:
            break
    next_idx = min(level + 1, len(LEVEL_TITLES) - 1)
    xp_ceil = LEVEL_TITLES[next_idx][0] if next_idx != level else xp_floor + 1
    return level, title, xp_floor, xp_ceil


# ── Moods ────────────────────────────────────────────────────────
MOODS = ["😴", "😞", "😐", "😊", "🌟"]
MOOD_LABELS = ["Exhausted", "Low", "Neutral", "Good", "Stellar"]

# ── Categories ───────────────────────────────────────────────────
LIBRARY_CATEGORIES = ["All", "Books", "Articles", "Notes", "Research", "Inspiration"]
TASK_PRIORITIES    = ["High", "Medium", "Low"]
TASK_SUBJECTS      = ["Mathematics", "Science", "Literature", "History",
                       "Programming", "Languages", "Arts", "Other"]

# ── Quest templates ──────────────────────────────────────────────
DAILY_QUEST_POOL = [
    {"name": "Study for 25 minutes",        "xp": 50, "category": "Study"},
    {"name": "Add a library item",           "xp": 30, "category": "Library"},
    {"name": "Write a journal entry",        "xp": 40, "category": "Journal"},
    {"name": "Complete 2 habits",            "xp": 35, "category": "Habits"},
    {"name": "Complete a study task",        "xp": 45, "category": "Study"},
    {"name": "Read for 15 minutes",          "xp": 25, "category": "Library"},
    {"name": "Reflect on today's mood",      "xp": 20, "category": "Journal"},
    {"name": "Mark a habit done",            "xp": 20, "category": "Habits"},
]

WEEKLY_QUEST_POOL = [
    {"name": "Maintain a 5-day streak",      "xp": 200, "category": "Habits"},
    {"name": "Add 5 library items",          "xp": 150, "category": "Library"},
    {"name": "Write 3 journal entries",      "xp": 180, "category": "Journal"},
    {"name": "Complete 10 study tasks",      "xp": 250, "category": "Study"},
    {"name": "Reach a new level",            "xp": 300, "category": "Study"},
    {"name": "Use the AI assistant 5 times", "xp": 120, "category": "Study"},
]

# ── Achievement definitions ──────────────────────────────────────
ACHIEVEMENTS = [
    {"id": "first_login",   "name": "First Light",         "icon": "🌙",
     "desc": "Logged in for the first time",               "xp_reward": 50},
    {"id": "first_journal", "name": "Dear Diary",          "icon": "📖",
     "desc": "Wrote your first journal entry",             "xp_reward": 30},
    {"id": "first_habit",   "name": "Creature of Habit",   "icon": "⭐",
     "desc": "Created your first habit",                   "xp_reward": 30},
    {"id": "first_task",    "name": "Quest Begun",         "icon": "⚔️",
     "desc": "Added your first study task",                "xp_reward": 30},
    {"id": "first_library", "name": "Bookworm",            "icon": "📚",
     "desc": "Added your first library item",              "xp_reward": 30},
    {"id": "level_2",       "name": "Moon Apprentice",     "icon": "🌛",
     "desc": "Reached level 2",                            "xp_reward": 100},
    {"id": "level_5",       "name": "Astral Scholar",      "icon": "🔮",
     "desc": "Reached level 5",                            "xp_reward": 250},
    {"id": "streak_7",      "name": "Seven Moons",         "icon": "🌕",
     "desc": "Maintained a 7-day login streak",            "xp_reward": 200},
    {"id": "library_10",    "name": "Grand Librarian",     "icon": "🏛️",
     "desc": "Added 10 items to your library",             "xp_reward": 150},
    {"id": "journal_7",     "name": "Soul Chronicler",     "icon": "✨",
     "desc": "Wrote 7 journal entries",                    "xp_reward": 200},
    {"id": "tasks_10",      "name": "Task Conqueror",      "icon": "🗡️",
     "desc": "Completed 10 study tasks",                   "xp_reward": 150},
    {"id": "xp_1000",       "name": "Cosmic Adept",        "icon": "💫",
     "desc": "Earned 1000 total XP",                       "xp_reward": 300},
]

# ── Pomodoro ─────────────────────────────────────────────────────
POMODORO_WORK_MINUTES  = 25
POMODORO_BREAK_MINUTES = 5
