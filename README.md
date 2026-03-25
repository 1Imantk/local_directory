# BizDirectory NG — Local Business & Startup Directory

A Flask web application that lets users **view**, **add**, **edit**, **rate**, and **delete**
local businesses and startups across Nigeria.

Built as Assignment 4 for **COS 202 — Building for the Web with Flask**  
Maryam Abacha American University of Nigeria (MAAUN)

---

## What the App Does

| Feature | Description |
|---|---|
| 📋 View all businesses | See every listed business in a card grid with colored category borders |
| 🔍 Search by name | Filter businesses by typing a name in the search bar |
| ↕ Sort businesses | Sort by Newest First, Oldest First, or A-Z |
| 📄 Pagination | Browse businesses 6 at a time with page navigation |
| 🕐 Recently Added | A live FIFO queue shows the 5 most recently added businesses |
| 📊 Category Summary | View total number of businesses per category |
| 🏷️ Filter by category | Click a category pill to filter the list |
| ⭐ Rate businesses | Submit a 1–5 star rating for each business |
| 🟢 Open/Closed Status | Toggle and display business operational status |
| ➕ Add a business | Register a new business with validation and confirmation page |
| ✏️ Edit a business | Update any business's details via a dedicated edit form |
| 📄 Business detail page | View full details at `/business/<id>` |
| 🗑 Delete | Remove a business from the directory |
| ↩ Undo Delete | Restore the last deleted business (uses a Stack / LIFO) |
| ℹ️ About | Explains the technical concepts used in the app |
| ❓ 404 Page | Custom error page with helpful links |

---

## Technical Concepts Demonstrated

- **OOP** — `Business` class with attributes and methods (`get_summary()`, `to_dict()`)
- **Queue (FIFO)** — `collections.deque` tracks the 5 most recently added businesses
- **Stack (LIFO)** — a list used as a stack enables undo-delete functionality
- **datetime API** — every business is automatically timestamped on registration
- **Flask** — Multiple routes connect Python logic to HTML templates via Jinja2
- **Form Validation** — Duplicate name prevention, required fields, and URL validation
- **Auto-incrementing IDs** — Each business gets a unique ID for detail/edit/delete routes
- **Unit Testing** — Queue and Stack logic tested with print-based assertions

---

## How to Run the App Locally (Beginner-Friendly)

Follow these steps exactly. You only need Python installed on your computer.

### Step 1 — Download or clone the project

If you have Git:
```bash
git clone https://github.com/1Imantk/local_directory.git
cd local_directory
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

### Step 7 — Run unit tests

```bash
python models_test.py
```

### Step 8 — Stop the app

Press `Ctrl + C` in the terminal.

---

## Project Structure

```
local_directory/
├── app.py              # Flask routes (home, add, edit, delete, rate, toggle status, etc.)
├── models.py           # OOP classes (Business, BusinessDirectory)
├── data.py             # Sample business data
├── models_test.py      # Unit tests for Queue and Stack logic
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── templates/
    ├── base.html       # Shared layout (nav, footer, flash messages, CSS)
    ├── index.html      # Home page — business grid, search, filters, pagination
    ├── add.html        # Add business form with character counter
    ├── edit.html       # Edit business form
    ├── confirmation.html # Registration success page
    ├── business_detail.html # Full business details with rating & status toggle
    ├── about.html      # About page
    └── 404.html        # Custom 404 error page
```

---

## Author

**Iman Rabiu** — COS 202 Student, MAAUN
