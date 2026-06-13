import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

DB_PATH = "data/tickets.db"

def fetch_tickets(query="SELECT * FROM tickets"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def log_change(ticket_id, change_type, old_value, new_value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO change_log (ticket_id, change_type, old_value, new_value, date_changed) VALUES (?, ?, ?, ?, ?)",
        (ticket_id, change_type, old_value, new_value, str(date.today()))
    )
    conn.commit()
    conn.close()

def view_tickets():
    root = tk.Tk()
    root.title("View & Manage Tickets")

    # Treeview table
    columns = ("ticket_id", "student_number", "student_name", "category", "description",
               "priority", "status", "date_logged", "closing_comment")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)

    def update_table(rows):
        for i in tree.get_children():
            tree.delete(i)
        if not rows:
            messagebox.showinfo("Info", "No tickets found.")
        else:
            for row in rows:
                tree.insert("", "end", values=row)

    update_table(fetch_tickets())

    # --- Task 7 Controls ---
    search_entry = tk.Entry(root)
    search_entry.pack(pady=5)

    def search():
        value = search_entry.get()
        rows = fetch_tickets(f"SELECT * FROM tickets WHERE student_number='{value}' OR ticket_id='{value}'")
        update_table(rows)

    tk.Button(root, text="Search", command=search).pack()

    status_combo = ttk.Combobox(root, values=["Open", "In Progress", "Resolved", "Closed"])
    status_combo.pack(pady=5)

    def filter_status():
        value = status_combo.get()
        rows = fetch_tickets(f"SELECT * FROM tickets WHERE status='{value}'")
        update_table(rows)

    tk.Button(root, text="Filter by Status", command=filter_status).pack()

    priority_combo = ttk.Combobox(root, values=["Low", "Medium", "High", "Critical"])
    priority_combo.pack(pady=5)

    def filter_priority():
        value = priority_combo.get()
        rows = fetch_tickets(f"SELECT * FROM tickets WHERE priority='{value}'")
        update_table(rows)

    tk.Button(root, text="Filter by Priority", command=filter_priority).pack()

    def sort_date():
        rows = fetch_tickets("SELECT * FROM tickets ORDER BY date_logged DESC")
        update_table(rows)

    tk.Button(root, text="Sort by Date", command=sort_date).pack()

    def sort_priority():
        rows = fetch_tickets("SELECT * FROM tickets ORDER BY priority")
        update_table(rows)

    tk.Button(root, text="Sort by Priority", command=sort_priority).pack()

    # --- Task 8 Update & Archive Controls ---
    update_status_combo = ttk.Combobox(root, values=["Open", "In Progress", "Resolved", "Closed"])
    update_status_combo.pack(pady=5)

    update_priority_combo = ttk.Combobox(root, values=["Low", "Medium", "High", "Critical"])
    update_priority_combo.pack(pady=5)

    comment_entry = tk.Entry(root, width=50)
    comment_entry.pack(pady=5)

    def update_ticket():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a ticket first.")
            return
        values = tree.item(selected[0], "values")
        ticket_id = values[0]

        new_status = update_status_combo.get() or values[6]
        new_priority = update_priority_combo.get() or values[5]
        new_comment = comment_entry.get() or values[8]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Log changes
        if new_status != values[6]:
            log_change(ticket_id, "Status Update", values[6], new_status)
        if new_priority != values[5]:
            log_change(ticket_id, "Priority Update", values[5], new_priority)
        if new_comment != values[8]:
            log_change(ticket_id, "Closing Comment", values[8], new_comment)

        cursor.execute("UPDATE tickets SET status=?, priority=?, closing_comment=? WHERE ticket_id=?",
                       (new_status, new_priority, new_comment, ticket_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Ticket {ticket_id} updated.")
        update_table(fetch_tickets())

    tk.Button(root, text="Update Ticket", command=update_ticket).pack(pady=5)

    def archive_ticket():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a ticket first.")
            return
        values = tree.item(selected[0], "values")
        ticket_id = values[0]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to archive ticket {ticket_id}?")
        if confirm:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            log_change(ticket_id, "Archived", "Active", "Deleted")
            cursor.execute("DELETE FROM tickets WHERE ticket_id=?", (ticket_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Archived", f"Ticket {ticket_id} archived.")
            update_table(fetch_tickets())

    tk.Button(root, text="Archive Ticket", command=archive_ticket).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    view_tickets()
