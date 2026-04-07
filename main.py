from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from fastapi.responses import FileResponse

app = FastAPI()

# -------- DATABASE --------
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, title TEXT, time TEXT)")
conn.commit()

# -------- REQUEST --------
class Query(BaseModel):
    query: str

# -------- TOOLS --------
def create_task(task):
    cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "pending"))
    conn.commit()
    return f"✅ Task added: {task}"

def add_event(title, time):
    cursor.execute("INSERT INTO events (title, time) VALUES (?, ?)", (title, time))
    conn.commit()
    return f"📅 Event scheduled: {title} at {time}"

def save_note(note):
    cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    return f"📝 Note saved: {note}"

# -------- SUB-AGENTS --------
def task_agent(text):
    return create_task(text)

def calendar_agent(text):
    return add_event(text, str(datetime.now()))

def notes_agent(text):
    return save_note(text)

# -------- MAIN AGENT --------
def main_agent(query):
    results = []

    if "task" in query.lower():
        results.append(task_agent(query))

    if "meeting" in query.lower() or "schedule" in query.lower():
        results.append(calendar_agent(query))

    if "note" in query.lower():
        results.append(notes_agent(query))

    if not results:
        results.append("🤖 Query understood but no action triggered.")

    return results

# -------- API --------
@app.post("/execute")
def execute(q: Query):
    result = main_agent(q.query)
    return {"response": result}

@app.get("/")
def home():
    return FileResponse("index.html")