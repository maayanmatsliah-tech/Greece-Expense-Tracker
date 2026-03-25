# Greece Expense Tracker

A personal finance web app built with Flask to track weekly spending and monitor progress toward a savings goal — originally built while studying abroad in Greece.
Live deployment can be found here: https://greece-expense-tracker.onrender.com/

---

## Motivation

I built this tool for myself while studying abroad to track how much I was spending each week and whether I was on pace to save the amount I had planned. Rather than using a spreadsheet, I wanted something that could calculate my progress automatically and visualize it.

---

## Features

- **Savings goal setup** — enter your starting budget and how much you want to save
- **Weekly spending log** — record how much you spent each week
- **Progress tracking** — see if you're on track to meet your savings goal
- **Adjusted budget calculator** — if you're off track, calculates what you need to spend per week going forward
- **Data persistence** — all data is saved to a CSV file so it persists between sessions
- **Visual charts** — bar chart and pie chart of your weekly spending breakdown
- **Reset option** — start over with a new savings goal at any time

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Data storage:** CSV
- **Visualization:** Matplotlib

---

## Project Structure

```
Greece-Expense-Tracker/
├── app.py                   # Flask routes and chart generation
├── savings_made_simple.py   # Core logic: CSV handling, tracking, summary stats
├── templates/
│   └── index.html           # Jinja2 HTML template
├── savings.csv              # Persistent data storage
└── README.md
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/maayanmatsliah-tech/Greece-Expense-Tracker.git
cd Greece-Expense-Tracker
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install flask matplotlib
```

**4. Run the app**
```bash
python3 app.py
```

**5. Open in your browser**
```
http://127.0.0.1:5500
```

---

## How It Works

1. On first launch, enter your starting budget and savings goal
2. Each week, log how much you spent
3. The app calculates your remaining budget, average weekly spending, and whether you're on track
4. If you're off track, it tells you how much you can spend per week going forward to still meet your goal
5. Charts update automatically as you log more weeks
6. All data is saved to `savings.csv` so your progress persists between sessions

---

## Author

**Maayan Matsliah**
Computer Science @ Northeastern University · AI Concentration

[LinkedIn](https://www.linkedin.com/in/maayan-matsliah-a523b3353/) · [GitHub](https://github.com/maayanmatsliah-tech)
