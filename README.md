# BizDirectory NG — Local Business & Startup Directory

A Flask web application that lets users **view**, **add**, **filter**, and **delete**
local businesses and startups across Nigeria.

Built as Assignment 4 for **COS 202 — Building for the Web with Flask**  
Maryam Abacha American University of Nigeria (MAAUN)

---

## What the App Does

| Feature | Description |
|---|---|
| 📋 View all businesses | See every listed business in a card grid |
| 🕐 Recently Added | A live FIFO queue shows the 5 most recently added businesses |
| ➕ Add a business | Fill in a form to register a new business with a timestamp |
| 🔍 Filter by category | Click a category pill to filter the list |
| 🗑 Delete | Remove a business from the directory |
| ↩ Undo Delete | Restore the last deleted business (uses a Stack / LIFO) |
| ℹ️ About | Explains the technical concepts used in the app |

---

## Technical Concepts Demonstrated

- **OOP** — `Business` class with `__init__`, `get_summary()`, and `to_dict()` methods  
- **Queue (FIFO)** — `collections.deque` tracks the 5 most recently added businesses  
- **Stack (LIFO)** — a list used as a stack enables undo-delete functionality  
- **datetime API** — every business is automatically timestamped on registration  
- **Flask** — 6 routes connect Python logic to HTML templates via Jinja2 forms  

---

## How to Run the App Locally (Beginner-Friendly)

Follow these steps exactly. You only need Python installed on your computer.

### Step 1 — Download or clone the project

If you have Git:
```bash
git clone https://github.com/YOUR_USERNAME/business_directory.git
cd business_directory
```

Or download the ZIP from GitHub and unzip it, then open a terminal inside the folder.

### Step 2 — Create a virtual environment

A virtual environment keeps the project's packages separate from the rest of your computer.

```bash
python3 -m venv venv
```

### Step 3 — Activate the virtual environment

**On Windows (Command Prompt):**
```
venv\Scripts\activate
```

**On Windows (WSL / Linux / macOS):**
```bash
source venv/bin/activate
```

You will see `(venv)` appear at the start of your terminal line — that means it worked.

### Step 4 — Install Flask

```bash
pip install -r requirements.txt
```

### Step 5 — Run the app

```bash
python app.py
```

You should see something like:
```
* Running on http://127.0.0.1:5000
```

### Step 6 — Open your browser

Go to **http://127.0.0.1:5000** and the app will load.

### Step 7 — Stop the app

Press `Ctrl + C` in the terminal.

---

## Project Structure

```
business_directory/
├── app.py              # Flask routes
├── models.py           # OOP classes (Business, BusinessDirectory)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── templates/
    ├── base.html       # Shared layout (nav, flash messages, CSS)
    ├── index.html      # Home page — business grid + queue + filters
    ├── add.html        # Add business form
    └── about.html      # About page
```

---

## Author

**Khaleel** — COS 202 Student, MAAUN
