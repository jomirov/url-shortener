import random, string, threading, sqlite3
from contextlib import asynccontextmanager
from datetime import datetime as dt
from fastapi import FastAPI

def get_db_path():
    return "database/database.db"

def generate_string():
    random_string = ''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k=8))
    return random_string

def cleanup_links():
    with sqlite3.connect(get_db_path()) as con:
        try:
            con.cursor().execute("DELETE FROM links WHERE created_at < datetime(?, '-1 day')", (dt.strftime(dt.now(), "%Y-%m-%d"),))
            con.commit()
            print("CLEANUP")
        except: print("Cleanup: got an error!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    e = threading.Event()
    t = threading.Thread(target=thread_cleanup, args=[e], daemon=True)
    t.start()
    yield
    e.set()
    t.join()

def thread_cleanup(e):
    while not e.isSet():
        cleanup_links()
        e.wait(60)