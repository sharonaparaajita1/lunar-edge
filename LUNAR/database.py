"""
LUNAR Database Layer
Uses SQLite for all persistent storage.
Tables are created automatically on first run.
"""

import sqlite3
import hashlib
import os
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path(__file__).parent / "database" / "lunar.db"


def _get_conn() -> sqlite3.Connection:
    """Return a thread-local SQLite connection with row-factory enabled."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create all tables if they don't already exist."""
    conn = _get_conn()
    cur = conn.cursor()

    # ── Users ────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            bio         TEXT DEFAULT '',
            avatar_color TEXT DEFAULT '#7c3aed',
            xp          INTEGER DEFAULT 0,
            streak      INTEGER DEFAULT 0,
            last_login  TEXT DEFAULT '',
            accent_color TEXT DEFAULT '#7c3aed',
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Notes ────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT NOT NULL,
            content    TEXT DEFAULT '',
            folder     TEXT DEFAULT 'General',
            pinned     INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ── Journal ──────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            entry_date TEXT NOT NULL,
            mood       INTEGER DEFAULT 2,
            content    TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ── Habits ───────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            name       TEXT NOT NULL,
            color      TEXT DEFAULT '#7c3aed',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_completions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id     INTEGER NOT NULL,
            user_id      INTEGER NOT NULL,
            completed_on TEXT NOT NULL,
            UNIQUE(habit_id, completed_on),
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    """)

    # ── Library ──────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS library (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            title        TEXT NOT NULL,
            item_type    TEXT DEFAULT 'Note',
            category     TEXT DEFAULT 'General',
            content      TEXT DEFAULT '',
            bookmarked   INTEGER DEFAULT 0,
            created_at   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ── Tasks ────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT NOT NULL,
            subject    TEXT DEFAULT 'Other',
            deadline   TEXT DEFAULT '',
            priority   TEXT DEFAULT 'Medium',
            completed  INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ── Quests ───────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quests (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            name        TEXT NOT NULL,
            quest_type  TEXT DEFAULT 'daily',
            xp_reward   INTEGER DEFAULT 50,
            category    TEXT DEFAULT 'Study',
            completed   INTEGER DEFAULT 0,
            reset_date  TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ── Achievements ─────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            achievement_id TEXT NOT NULL,
            unlocked_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(user_id, achievement_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ── Chat History ─────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            role       TEXT NOT NULL,
            content    TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ── Helpers ───────────────────────────────────────────────────────

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── User operations ───────────────────────────────────────────────

def create_user(username: str, email: str, password: str) -> dict | None:
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, _hash_password(password))
        )
        conn.commit()
        return get_user_by_id(cur.lastrowid)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict | None:
    conn = _get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def authenticate_user(email: str, password: str) -> dict | None:
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, _hash_password(password))
    ).fetchone()
    conn.close()
    if row:
        update_streak(row["id"])
        return get_user_by_id(row["id"])
    return None


def update_streak(user_id: int) -> None:
    conn = _get_conn()
    user = conn.execute("SELECT last_login, streak FROM users WHERE id = ?", (user_id,)).fetchone()
    today = date.today().isoformat()
    if user:
        last = user["last_login"]
        streak = user["streak"]
        if last == today:
            pass
        elif last == (date.today().replace(day=date.today().day - 1)).isoformat() if date.today().day > 1 else "":
            streak += 1
        else:
            streak = 1 if last != today else streak
        conn.execute("UPDATE users SET last_login = ?, streak = ? WHERE id = ?",
                     (today, streak, user_id))
        conn.commit()
    conn.close()


def update_user_xp(user_id: int, xp_delta: int) -> dict:
    conn = _get_conn()
    conn.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_delta, user_id))
    conn.commit()
    conn.close()
    return get_user_by_id(user_id)


def update_user_profile(user_id: int, **kwargs) -> dict:
    allowed = {"username", "bio", "avatar_color", "accent_color"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return get_user_by_id(user_id)
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    conn = _get_conn()
    conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?",
                 (*fields.values(), user_id))
    conn.commit()
    conn.close()
    return get_user_by_id(user_id)


# ── Notes ─────────────────────────────────────────────────────────

def get_notes(user_id: int, folder: str | None = None, search: str = "") -> list[dict]:
    conn = _get_conn()
    query = "SELECT * FROM notes WHERE user_id = ?"
    params: list = [user_id]
    if folder and folder != "All":
        query += " AND folder = ?"
        params.append(folder)
    if search:
        query += " AND (title LIKE ? OR content LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    query += " ORDER BY pinned DESC, updated_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_note_folders(user_id: int) -> list[str]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT DISTINCT folder FROM notes WHERE user_id = ? ORDER BY folder",
        (user_id,)
    ).fetchall()
    conn.close()
    return ["All"] + [r["folder"] for r in rows]


def create_note(user_id: int, title: str, content: str, folder: str) -> dict:
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO notes (user_id, title, content, folder) VALUES (?, ?, ?, ?)",
        (user_id, title, content, folder)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


def update_note(note_id: int, **kwargs) -> None:
    allowed = {"title", "content", "folder", "pinned"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    fields["updated_at"] = datetime.now().isoformat()
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    conn = _get_conn()
    conn.execute(f"UPDATE notes SET {set_clause} WHERE id = ?",
                 (*fields.values(), note_id))
    conn.commit()
    conn.close()


def delete_note(note_id: int) -> None:
    conn = _get_conn()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


# ── Journal ───────────────────────────────────────────────────────

def get_journal_entry(user_id: int, entry_date: str) -> dict | None:
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM journal WHERE user_id = ? AND entry_date = ?",
        (user_id, entry_date)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def upsert_journal_entry(user_id: int, entry_date: str, mood: int, content: str) -> dict:
    conn = _get_conn()
    existing = conn.execute(
        "SELECT id FROM journal WHERE user_id = ? AND entry_date = ?",
        (user_id, entry_date)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE journal SET mood = ?, content = ? WHERE id = ?",
            (mood, content, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO journal (user_id, entry_date, mood, content) VALUES (?, ?, ?, ?)",
            (user_id, entry_date, mood, content)
        )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM journal WHERE user_id = ? AND entry_date = ?",
        (user_id, entry_date)
    ).fetchone()
    conn.close()
    return dict(row)


def get_journal_entries(user_id: int) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM journal WHERE user_id = ? ORDER BY entry_date DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_journal_streak(user_id: int) -> int:
    entries = get_journal_entries(user_id)
    if not entries:
        return 0
    streak = 0
    check_date = date.today()
    date_set = {e["entry_date"] for e in entries}
    while check_date.isoformat() in date_set:
        streak += 1
        check_date = check_date.replace(day=check_date.day - 1) if check_date.day > 1 else check_date
        if streak > 365:
            break
    return streak


# ── Habits ────────────────────────────────────────────────────────

def get_habits(user_id: int) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM habits WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_habit(user_id: int, name: str, color: str = "#7c3aed") -> dict:
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO habits (user_id, name, color) VALUES (?, ?, ?)",
        (user_id, name, color)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM habits WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


def delete_habit(habit_id: int) -> None:
    conn = _get_conn()
    conn.execute("DELETE FROM habit_completions WHERE habit_id = ?", (habit_id,))
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()


def toggle_habit_completion(habit_id: int, user_id: int, on_date: str) -> bool:
    """Toggle completion. Returns True if now completed."""
    conn = _get_conn()
    existing = conn.execute(
        "SELECT id FROM habit_completions WHERE habit_id = ? AND completed_on = ?",
        (habit_id, on_date)
    ).fetchone()
    if existing:
        conn.execute("DELETE FROM habit_completions WHERE id = ?", (existing["id"],))
        completed = False
    else:
        conn.execute(
            "INSERT INTO habit_completions (habit_id, user_id, completed_on) VALUES (?, ?, ?)",
            (habit_id, user_id, on_date)
        )
        completed = True
    conn.commit()
    conn.close()
    return completed


def get_habit_completions(user_id: int, days: int = 7) -> dict[int, list[str]]:
    """Returns {habit_id: [completed_dates]} for last N days."""
    conn = _get_conn()
    rows = conn.execute(
        """SELECT habit_id, completed_on FROM habit_completions
           WHERE user_id = ?
           ORDER BY completed_on DESC""",
        (user_id,)
    ).fetchall()
    conn.close()
    result: dict[int, list[str]] = {}
    for row in rows:
        result.setdefault(row["habit_id"], []).append(row["completed_on"])
    return result


# ── Library ───────────────────────────────────────────────────────

def get_library_items(user_id: int, category: str = "All",
                      item_type: str = "", search: str = "") -> list[dict]:
    conn = _get_conn()
    query = "SELECT * FROM library WHERE user_id = ?"
    params: list = [user_id]
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    if item_type:
        query += " AND item_type = ?"
        params.append(item_type)
    if search:
        query += " AND (title LIKE ? OR content LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    query += " ORDER BY bookmarked DESC, created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_library_item(user_id: int, title: str, item_type: str,
                        category: str, content: str) -> dict:
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO library (user_id, title, item_type, category, content) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, item_type, category, content)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM library WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


def toggle_bookmark(item_id: int) -> None:
    conn = _get_conn()
    conn.execute("UPDATE library SET bookmarked = 1 - bookmarked WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def delete_library_item(item_id: int) -> None:
    conn = _get_conn()
    conn.execute("DELETE FROM library WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# ── Tasks ─────────────────────────────────────────────────────────

def get_tasks(user_id: int) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY completed ASC, priority DESC, deadline ASC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_task(user_id: int, title: str, subject: str,
                deadline: str, priority: str) -> dict:
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO tasks (user_id, title, subject, deadline, priority) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, subject, deadline, priority)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


def toggle_task(task_id: int) -> bool:
    conn = _get_conn()
    row = conn.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
    new_val = 0 if row["completed"] else 1
    conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_val, task_id))
    conn.commit()
    conn.close()
    return bool(new_val)


def delete_task(task_id: int) -> None:
    conn = _get_conn()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# ── Quests ────────────────────────────────────────────────────────

def get_quests(user_id: int, quest_type: str) -> list[dict]:
    today = date.today().isoformat()
    reset = today if quest_type == "daily" else _week_start()
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM quests WHERE user_id = ? AND quest_type = ? AND reset_date = ?",
        (user_id, quest_type, reset)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def seed_quests(user_id: int) -> None:
    """Seed daily/weekly quests if none exist for today/this week."""
    import random
    from config import DAILY_QUEST_POOL, WEEKLY_QUEST_POOL

    today = date.today().isoformat()
    week  = _week_start()

    daily   = get_quests(user_id, "daily")
    weekly  = get_quests(user_id, "weekly")

    conn = _get_conn()
    if not daily:
        pool = random.sample(DAILY_QUEST_POOL, min(3, len(DAILY_QUEST_POOL)))
        for q in pool:
            conn.execute(
                "INSERT INTO quests (user_id, name, quest_type, xp_reward, category, reset_date) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, q["name"], "daily", q["xp"], q["category"], today)
            )
    if not weekly:
        pool = random.sample(WEEKLY_QUEST_POOL, min(2, len(WEEKLY_QUEST_POOL)))
        for q in pool:
            conn.execute(
                "INSERT INTO quests (user_id, name, quest_type, xp_reward, category, reset_date) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, q["name"], "weekly", q["xp"], q["category"], week)
            )
    conn.commit()
    conn.close()


def complete_quest(quest_id: int, user_id: int) -> int:
    """Mark quest complete, return XP earned."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT xp_reward, completed FROM quests WHERE id = ?", (quest_id,)
    ).fetchone()
    if row and not row["completed"]:
        conn.execute("UPDATE quests SET completed = 1 WHERE id = ?", (quest_id,))
        conn.execute("UPDATE users SET xp = xp + ? WHERE id = ?",
                     (row["xp_reward"], user_id))
        conn.commit()
        conn.close()
        return row["xp_reward"]
    conn.close()
    return 0


def _week_start() -> str:
    today = date.today()
    return (today - __import__("datetime").timedelta(days=today.weekday())).isoformat()


# ── Achievements ──────────────────────────────────────────────────

def get_unlocked_achievements(user_id: int) -> list[str]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT achievement_id FROM achievements WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn.close()
    return [r["achievement_id"] for r in rows]


def unlock_achievement(user_id: int, achievement_id: str, xp_reward: int = 0) -> bool:
    """Returns True if newly unlocked."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO achievements (user_id, achievement_id) VALUES (?, ?)",
            (user_id, achievement_id)
        )
        if xp_reward:
            conn.execute("UPDATE users SET xp = xp + ? WHERE id = ?",
                         (xp_reward, user_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def check_and_unlock_achievements(user_id: int) -> list[str]:
    """Check conditions and unlock any newly earned achievements. Returns new achievement ids."""
    from config import ACHIEVEMENTS
    unlocked = get_unlocked_achievements(user_id)
    user     = get_user_by_id(user_id)
    new_ones = []

    conditions = {
        "first_login":   True,
        "first_journal": bool(get_journal_entries(user_id)),
        "first_habit":   bool(get_habits(user_id)),
        "first_task":    bool(get_tasks(user_id)),
        "first_library": bool(get_library_items(user_id)),
        "level_2":       (user["xp"] if user else 0) >= 100,
        "level_5":       (user["xp"] if user else 0) >= 600,
        "streak_7":      (user["streak"] if user else 0) >= 7,
        "library_10":    len(get_library_items(user_id)) >= 10,
        "journal_7":     len(get_journal_entries(user_id)) >= 7,
        "tasks_10":      sum(1 for t in get_tasks(user_id) if t["completed"]) >= 10,
        "xp_1000":       (user["xp"] if user else 0) >= 1000,
    }

    for ach in ACHIEVEMENTS:
        aid = ach["id"]
        if aid not in unlocked and conditions.get(aid, False):
            if unlock_achievement(user_id, aid, ach.get("xp_reward", 0)):
                new_ones.append(aid)

    return new_ones


# ── Chat History ──────────────────────────────────────────────────

def get_chat_history(user_id: int, limit: int = 50) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM chat_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return list(reversed([dict(r) for r in rows]))


def add_chat_message(user_id: int, role: str, content: str) -> None:
    conn = _get_conn()
    conn.execute(
        "INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)",
        (user_id, role, content)
    )
    conn.commit()
    conn.close()


def clear_chat_history(user_id: int) -> None:
    conn = _get_conn()
    conn.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ── Analytics ─────────────────────────────────────────────────────

def get_analytics(user_id: int) -> dict:
    conn = _get_conn()
    total_tasks     = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,)).fetchone()[0]
    completed_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1", (user_id,)).fetchone()[0]
    total_library   = conn.execute("SELECT COUNT(*) FROM library WHERE user_id = ?", (user_id,)).fetchone()[0]
    total_journal   = conn.execute("SELECT COUNT(*) FROM journal WHERE user_id = ?", (user_id,)).fetchone()[0]
    total_habits    = conn.execute("SELECT COUNT(*) FROM habits WHERE user_id = ?", (user_id,)).fetchone()[0]
    total_notes     = conn.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,)).fetchone()[0]

    # XP over last 7 days (from quest completions approximation)
    quest_rows = conn.execute(
        "SELECT reset_date, SUM(xp_reward) FROM quests WHERE user_id = ? AND completed = 1 GROUP BY reset_date",
        (user_id,)
    ).fetchall()
    xp_by_date = {r[0]: r[1] for r in quest_rows}

    # Habit completions by date (last 14 days)
    habit_rows = conn.execute(
        "SELECT completed_on, COUNT(*) FROM habit_completions WHERE user_id = ? GROUP BY completed_on",
        (user_id,)
    ).fetchall()
    habits_by_date = {r[0]: r[1] for r in habit_rows}

    conn.close()
    return {
        "total_tasks":     total_tasks,
        "completed_tasks": completed_tasks,
        "total_library":   total_library,
        "total_journal":   total_journal,
        "total_habits":    total_habits,
        "total_notes":     total_notes,
        "xp_by_date":      xp_by_date,
        "habits_by_date":  habits_by_date,
    }
