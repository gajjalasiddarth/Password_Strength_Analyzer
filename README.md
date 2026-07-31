# 🔐 Password Strength Analyzer

## 📌 Project Overview

Password Strength Analyzer is a Python-based desktop application that checks the strength of a password using various security rules. It provides instant feedback, suggests improvements, and stores password analysis history in a SQLite database.

## 🚀 Features

- Check password strength
- Security score (0–5)
- Weak, Medium, and Strong classification
- Password improvement suggestions
- Show/Hide password
- Generate strong password
- Copy password to clipboard
- Progress bar for password strength
- Save password history using SQLite
- View password history

## 🛠 Technologies Used

- Python
- Tkinter
- SQLite3
- Regular Expressions (re)
- Pyperclip

## 📂 Project Structure

```
password-strength-analyzer/
│── gui.py
│── app.py
│── passwords.db
│── README.md
│── requirements.txt
```

## ▶️ How to Run

1. Clone or download the project.
2. Install the required package:

```bash
pip install pyperclip
```

3. Run the application:

```bash
python gui.py
```

## 📋 Password Rules

A strong password should contain:

- At least 8 characters
- One uppercase letter
- One lowercase letter
- One number
- One special character

## 📊 Features Demonstrated

- Password validation
- Password strength analysis
- GUI development with Tkinter
- SQLite database integration
- Password generation
- Clipboard functionality
- Progress bar implementation

## 📜 Future Improvements

- Password hashing
- Dark mode
- Export password history
- Advanced password entropy analysis

## 👨‍💻 Author

**Gajjala Siddarth**

B.Tech – Computer Science & Engineering (Networks)

Kakatiya Institute of Technology and Science, Warangal
