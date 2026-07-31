import tkinter as tk
from tkinter import ttk
import re
import sqlite3
import random
import string
from datetime import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS password_history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
password TEXT,
strength TEXT,
checked_at TEXT
)
""")
conn.commit()


def check_password():

    password = password_entry.get()

    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("✔ Minimum 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("✔ Add Uppercase Letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("✔ Add Lowercase Letter")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("✔ Add Number")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("✔ Add Special Character")

    if score <= 2:
        strength = "WEAK"
        color = "red"
    elif score <= 4:
        strength = "MEDIUM"
        color = "orange"
    else:
        strength = "STRONG"
        color = "green"

    result_label.config(
        text=f"Strength : {strength}\nSecurity Score : {score}/5",
        fg=color
    )

    # Update Progress Bar
    progress["value"] = score

    if suggestions:
        suggestion_label.config(text="\n".join(suggestions))
    else:
        suggestion_label.config(
            text="Excellent! Your password is secure."
        )

    cursor.execute(
        "INSERT INTO password_history(password, strength, checked_at) VALUES (?, ?, ?)",
        (
            password,
            strength,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()


def clear():
    password_entry.delete(0, tk.END)
    result_label.config(text="")
    suggestion_label.config(text="")
    progress["value"] = 0


def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_btn.config(text="Hide Password")
    else:
        password_entry.config(show="*")
        show_btn.config(text="Show Password")


def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(chars) for _ in range(12))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def copy_password():
    password = password_entry.get()

    if password:
        import pyperclip
        pyperclip.copy(password)
        suggestion_label.config(
            text="✅ Password copied to clipboard!",
            fg="green"
        )
    else:
        suggestion_label.config(
            text="⚠ Please generate or enter a password first.",
            fg="red"
        )


def view_history():


    history_window = tk.Toplevel(root)
    history_window.title(" Password History")
    history_window.geometry("850x450")
    history_window.configure(bg="#f2f6fc")

    title = tk.Label(
        history_window,
        text="Password History",
        font=("Arial", 18, "bold"),
        bg="#f2f6fc",
        fg="#003366"
    )
    title.pack(pady=10)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        font=("Arial", 11),
        rowheight=28,
        background="white",
        foreground="black",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 12, "bold"),
        background="#003366",
        foreground="white"
    )

    frame = tk.Frame(history_window, bg="#f2f6fc")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    columns = ("ID", "Password", "Strength", "Checked At")

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(command=tree.yview)

    tree.heading("ID", text="ID")
    tree.heading("Password", text="Password")
    tree.heading("Strength", text="Strength")
    tree.heading("Checked At", text="Checked At")

    tree.column("ID", width=60, anchor="center")
    tree.column("Password", width=250, anchor="center")
    tree.column("Strength", width=120, anchor="center")
    tree.column("Checked At", width=250, anchor="center")

    tree.tag_configure("even", background="white")
    tree.tag_configure("odd", background="#EAF4FF")

    cursor.execute("""
        SELECT id, password, strength, checked_at
        FROM password_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    if rows:
        for index, row in enumerate(rows):
            tag = "even" if index % 2 == 0 else "odd"
            tree.insert("", tk.END, values=row, tags=(tag,))
    else:
        tree.insert("", tk.END, values=("", "No History Found", "", ""))

    tree.pack(fill="both", expand=True)

    close_btn = tk.Button(
        history_window,
        text="Close",
        command=history_window.destroy,
        bg="#f44336",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15
    )
    close_btn.pack(pady=10)

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("520x560")
root.configure(bg="#f2f6fc")

title = tk.Label(
    root,
    text="🔐 PASSWORD STRENGTH ANALYZER",
    font=("Arial", 18, "bold"),
    bg="#f2f6fc",
    fg="#003366"
)
title.pack(pady=15)

tk.Label(
    root,
    text="Enter Password",
    font=("Arial", 12),
    bg="#f2f6fc"
).pack()

password_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 14),
    show="*"
)
password_entry.pack(pady=8)

show_btn = tk.Button(
    root,
    text="Show Password",
    command=toggle_password,
    bg="#4CAF50",
    fg="white",
    width=18
)
show_btn.pack()

generate_btn = tk.Button(
    root,
    text="Generate Strong Password",
    command=generate_password,
    bg="#9C27B0",
    fg="white",
    font=("Arial", 11, "bold"),
    width=22
)
generate_btn.pack(pady=8)
copy_btn = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    bg="#FF9800",
    fg="white",
    font=("Arial", 11, "bold"),
    width=22
)
copy_btn.pack(pady=5)
history_btn = tk.Button(
    root,
    text="View Password History",
    command=view_history,
    bg="#673AB7",
    fg="white",
    font=("Arial", 11, "bold"),
    width=22
)
history_btn.pack(pady=5)

tk.Button(
    root,
    text="Check Strength",
    command=check_password,
    bg="#2196F3",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(pady=12)

tk.Button(
    root,
    text="Clear",
    command=clear,
    bg="#f44336",
    fg="white",
    width=20
).pack()

result_label = tk.Label(
    root,
    font=("Arial", 14, "bold"),
    bg="#f2f6fc"
)
result_label.pack(pady=12)
# Progress Bar
progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="determinate",
    maximum=5
)
progress.pack(pady=10)

suggestion_label = tk.Label(
    root,
    font=("Arial", 11),
    justify="left",
    bg="#f2f6fc",
    fg="blue"
)
suggestion_label.pack()

root.mainloop()

conn.close()