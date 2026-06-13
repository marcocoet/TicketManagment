from dataclasses import dataclass
from datetime import date
import sqlite3

@dataclass
class Ticket:
    ticket_id: str
    student_number: str
    student_name: str
    category: str
    description: str
    priority: str
    status: str = "Open"
    date_logged: str = str(date.today())
    closing_comment: str = ""

def generate_ticket_id():
    conn = sqlite3.connect("data/tickets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ticket_id FROM tickets ORDER BY ticket_id DESC LIMIT 1")
    last = cursor.fetchone()
    conn.close()

    if last:
        num = int(last[0][1:]) + 1
        return f"T{num:03d}"
    else:
        return "T001"
