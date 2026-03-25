"""
Maayan Matsliah
2025
Savings Made Simple
"""
import csv
import os

FILENAME = "savings_made_simple.csv"

# -----------------------
# CSV HANDLING
# -----------------------

def create_csv_if_not_exists(filename=FILENAME):
    """Create the CSV file with required structure if it doesn't already exist."""
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["StartMoney", "FinishMoney"])
            writer.writerow(["", ""])
            writer.writerow(["Week", "MoneySpent", "RemainingBudget"])


def read_csv(filename=FILENAME):
    if not os.path.exists(filename):
        return 0.0, 0, [], [], None, None

    starting_money = None
    finishing_money = None
    total_spent = 0.0
    last_week = 0
    weekly_spending_list = []
    week_numbers = []

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        if len(rows) >= 2 and rows[1][0] and rows[1][1]:
            try:
                starting_money = float(rows[1][0])
                finishing_money = float(rows[1][1])
            except ValueError:
                pass

        for row in rows[2:]:
            if len(row) >= 3 and row[0]:
                try:
                    week = int(row[0])
                    spent = float(row[1])
                except ValueError:
                    continue

                weekly_spending_list.append(spent)
                week_numbers.append(week)
                total_spent += spent
                last_week = week

    return total_spent, last_week, weekly_spending_list, week_numbers, starting_money, finishing_money


def update_start_finish_csv(starting_money, finishing_money, filename=FILENAME):
    with open(filename, "r", newline="") as csvfile:
        rows = list(csv.reader(csvfile))

    while len(rows) < 2:
        rows.append(["", ""])
    rows[1][0] = str(starting_money)
    rows[1][1] = str(finishing_money)

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def append_to_csv(week, money_spent, remaining_budget, filename=FILENAME):
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([week, money_spent, f"{remaining_budget:.2f}"])


# -----------------------
# WEEKLY TRACKING LOGIC
# -----------------------

def calculate_week(start, finish, weekly_spending_list, week_number, weekly_expense):
    total_spent = sum(weekly_spending_list)
    money_available = start - finish - total_spent - weekly_expense
    weekly_spending_list.append(weekly_expense)
    return money_available, weekly_spending_list


def get_summary(start, finish, weekly_spending_list):
    total_spent = sum(weekly_spending_list)
    money_left = start - total_spent

    weeks_total = 13
    weeks_passed = len(weekly_spending_list)

    avg_weekly = total_spent / weeks_passed if weeks_passed > 0 else 0
    necessary_avg = (start - finish) / weeks_total
    on_track = avg_weekly <= necessary_avg

    if total_spent <= (start - finish):
        remaining_allowed = (start - finish) - total_spent
        weeks_remaining = weeks_total - weeks_passed
        adjusted_avg = remaining_allowed / weeks_remaining if weeks_remaining > 0 else 0
    else:
        adjusted_avg = None

    return {
        "total_spent": total_spent,
        "money_left": money_left,
        "avg_weekly": avg_weekly,
        "necessary_avg": necessary_avg,
        "on_track": on_track,
        "adjusted_avg": adjusted_avg,
        "weeks_passed": weeks_passed
    }