import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import csv

DB_PATH = "data/tickets.db"

def get_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE Closing_comment='Open'")
    open_tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE Closing_comment='Closed'")
    closed_tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority IN ('High','Critical')")
    high_critical_tickets = cursor.fetchone()[0]

    conn.close()
    return total_tickets, open_tickets, closed_tickets, high_critical_tickets

def export_report(total, open_t, closed, high_critical):
    with open("data/report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Count"])
        writer.writerow(["Total Tickets", total])
        writer.writerow(["Open Tickets", open_t])
        writer.writerow(["Closed Tickets", closed])
        writer.writerow(["High/Critical Tickets", high_critical])
    messagebox.showinfo("Export", "Report exported to report.csv")

def show_report():
    root = tk.Tk()
    root.title("Ticket Report & Dashboard")

    total, open_t, closed, high_critical = get_counts()

    # --- Dashboard Cards ---
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text=f"Total Tickets: {total}", font=("Arial", 14), bg="lightblue").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(frame, text=f"Open Tickets: {open_t}", font=("Arial", 14), bg="lightgreen").grid(row=0, column=1, padx=10, pady=10)
    tk.Label(frame, text=f"Closed Tickets: {closed}", font=("Arial", 14), bg="lightgrey").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(frame, text=f"High/Critical Tickets: {high_critical}", font=("Arial", 14), bg="salmon").grid(row=1, column=1, padx=10, pady=10)

    # --- Report Screen ---
    report_text = tk.Text(root, width=60, height=10)
    report_text.pack(pady=10)
    report_text.insert(tk.END, "Ticket Report Summary\n")
    report_text.insert(tk.END, f"Total Tickets: {total}\n")
    report_text.insert(tk.END, f"Open Tickets: {open_t}\n")
    report_text.insert(tk.END, f"Closed Tickets: {closed}\n")
    report_text.insert(tk.END, f"High/Critical Tickets: {high_critical}\n")

    # --- Export Button ---
    tk.Button(root, text="Export Report to CSV", command=lambda: export_report(total, open_t, closed, high_critical)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    show_report()
