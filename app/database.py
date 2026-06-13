import sqlite3

def init_db():
    conn = sqlite3.connect("data/tickets.db")
    cursor = conn.cursor()

    # Create tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            student_number TEXT NOT NULL,
            student_name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            date_logged TEXT NOT NULL,
            closing_comment TEXT
        );
    """)

    # Create change_log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS change_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            change_type TEXT,
            old_value TEXT,
            new_value TEXT,
            date_changed TEXT
        );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
