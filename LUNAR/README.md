# 🌙 LUNAR — Celestial Productivity Platform

> *Your enchanted sanctuary for learning, growth, and self-discovery.*

LUNAR is a premium AI-powered productivity platform with a magical dark fantasy aesthetic — built entirely in Python and Streamlit. It transforms your daily study and growth routines into an enchanted adventure through gamification, beautiful design, and seamless tracking.

---

## ✨ Features

| Module | Description |
|---|---|
| 🏠 **Dashboard** | XP level, streak counter, daily quests, mood selector, library stats |
| 🤖 **AI Assistant** | Chat interface with cosmic AI responses (OpenAI-ready placeholder) |
| 📚 **Infinite Library** | Store books, articles, notes with search, categories, and bookmarks |
| 📅 **Study Planner** | Tasks with subjects, priorities, deadlines + Pomodoro timer |
| 📝 **Notes** | Folder-organised notes with pin, search, and rich editing |
| ✍️ **Journal** | Daily reflection with mood tracking, prompts, and writing streak |
| ⚡ **Habit Tracker** | 7-day grid, streak calculation, Plotly charts, XP rewards |
| ⚔️ **Quest System** | Auto-generated daily/weekly quests with XP rewards and level-up |
| 🏆 **Achievements** | 12 unlockable badges triggered by real activity milestones |
| 📊 **Analytics** | Plotly charts: XP over time, habit completion, task progress, library breakdown |
| 👤 **Profile** | Avatar, bio, level badge, full stats, achievement showcase |
| ⚙️ **Settings** | Accent colours, music toggle, notification preferences |

---

## 🚀 Installation

### Requirements
- Python 3.12+
- pip

### 1. Clone / download the project
```bash
cd LUNAR
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## 🗂️ Project Structure

```
LUNAR/
│
├── app.py                    ← Entry point + Dashboard + Sidebar
├── requirements.txt          ← Python dependencies
├── README.md
├── config.py                 ← App constants, XP, levels, achievements
├── database.py               ← SQLite layer (auto-creates all tables)
│
├── pages/                    ← Streamlit multi-page app
│   ├── Login.py              ← Login & Sign Up
│   ├── Dashboard.py          ← Redirect to app.py
│   ├── AI_Assistant.py       ← Chat interface
│   ├── Infinite_Library.py   ← Book/article/note manager
│   ├── Study_Planner.py      ← Tasks + Pomodoro timer
│   ├── Notes.py              ← Rich notes with folders
│   ├── Journal.py            ← Daily journal + mood tracker
│   ├── Habit_Tracker.py      ← Habit grid + Plotly charts
│   ├── Quest_System.py       ← Daily/weekly quest gamification
│   ├── Achievements.py       ← Badge showcase
│   ├── Analytics.py          ← Plotly analytics dashboard
│   ├── Profile.py            ← User profile + stats
│   └── Settings.py           ← Preferences + danger zone
│
├── assets/
│   └── music/                ← Drop ambient.mp3 here for background music
│
├── database/                 ← SQLite database file (auto-created)
│
├── utils/
│   └── helpers.py            ← Shared utilities, AI response generator
│
└── styles/
    └── theme.py              ← Global CSS injection (glassmorphism, stars, colours)
```

---

## 🎮 Gamification

| Action | XP Earned |
|---|---|
| Complete a quest | +30–300 XP |
| Finish a study task | +25 XP |
| Write a journal entry | +20 XP |
| Add a library item | +15 XP |
| Check off a habit | +10 XP |
| Complete a Pomodoro session | +30 XP |

### Levels
| XP | Title |
|---|---|
| 0 | Stargazer |
| 100 | Moon Apprentice |
| 300 | Lunar Scholar |
| 600 | Celestial Sage |
| 1000 | Astral Wizard |
| 1500 | Cosmic Archon |
| 2500 | Ethereal Oracle |
| 4000 | LUNAR Master |

---

## 🤖 Enabling Real AI (OpenAI)

In `utils/helpers.py`, replace the `generate_ai_response` function with:

```python
import openai, os
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_response(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are LUNAR's AI — wise, cosmic, and encouraging."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
```

Then add your key to a `.env` file:
```
OPENAI_API_KEY=sk-...
```

---

## 🎵 Background Music

Place any ambient MP3 file at:
```
LUNAR/assets/music/ambient.mp3
```
Then toggle "Enable ambient music" in Settings.

---

## 🖥️ VS Code Compatibility

LUNAR runs perfectly in VS Code on Windows:

1. Open the `LUNAR/` folder in VS Code
2. Open the integrated terminal (`Ctrl+\``)
3. Run: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Click the `localhost:8501` link in the terminal

No additional configuration required.

---

## 📸 Screenshots

> Add screenshots here after first run.

- Landing page with animated moon
- Dashboard with XP, streak, quests
- AI Assistant chat interface
- Library grid view
- Habit Tracker 7-day grid
- Analytics charts
- Achievement badges

---

## 🔮 Future Improvements

- [ ] Real-time OpenAI streaming responses
- [ ] Collaborative study rooms (multi-user)
- [ ] Spaced repetition flashcard system
- [ ] Calendar sync (Google Calendar API)
- [ ] Mobile-responsive PWA wrapper
- [ ] Custom theme editor with live preview
- [ ] Voice journaling with Whisper transcription
- [ ] Study group leaderboard

---

## 🛠️ Tech Stack

- **Python 3.12+** — Core language
- **Streamlit** — Web framework
- **SQLite** — Local database (zero setup)
- **Plotly** — Interactive charts
- **Pandas** — Data processing
- **Pillow** — Image handling
- **OpenAI** — AI integration (placeholder)

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*✦ Built with magic and Python ✦*
