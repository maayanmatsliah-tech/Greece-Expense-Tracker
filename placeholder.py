"""
Maayan Matsliah
2025
Savings Made Simple
"""

import csv
import os
import matplotlib.pyplot as plt
import numpy as np

FILENAME = "savings_made_simple.csv"

"""
CSV HANDLING --------------------------------------------------------------------------------
"""

def create_csv_if_not_exists(filename = FILENAME):
    """Create the CSV file with required structure if it doesn't already exist."""
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["StartMoney", "FinishMoney"])
            writer.writerow(["", ""])
            writer.writerow(["Week", "MoneySpent", "RemainingBudget"])


def read_csv(filename = FILENAME):

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


def update_start_finish_csv(starting_money, finishing_money):
    with open(FILENAME, "r", newline= "") as csvfile:
        rows = list(csv.reader(csvfile))

    while len(rows) < 2:
        rows.append(["", ""])
    rows[1][0] = str(starting_money)
    rows[1][1] = str(finishing_money)

    with open(FILENAME, "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def append_to_csv(week, money_spent, remaining_budget, filename = FILENAME):
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        remaining_formatted = f"{remaining_budget:.2f}"
        writer.writerow([week, money_spent, remaining_formatted])


"""
INPUT VALIDATION  ------------------------------------------------------------------------------
"""

def checking_for_float(question):
    while True:
        try:
            value = float(input(question))
            if value >= 0:
                return value
            else:
                print("Please enter an amount greater than 0")
        except ValueError:
            print("Invalid input. Please enter a number.")


def checking_for_smaller_num(max_value, question):
    while True:
        try:
            value = float(input(question))
            if value < 0:
                print("Please enter an amount greater than 0")
            elif value <= max_value:
                return value
            else:
                print("Invalid input. This amount must be less than or equal to the amount of money you have to start with.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def ask_continue(question):
    while True:
        cont = input(question)
        cont = cont.lower().strip()
        if cont == "yes":
            return True
        elif cont == "no":
            return False
        else:
            print("Invalid input. Please enter yes or no.")

"""
CORE TRACKING LOGIC  ---------------------------------------------------------------------------
"""

def money_tracker(start, finish, total_spent, last_week, weekly_spending_list, week_numbers):

    money_available = start - finish - total_spent
    weeks_in_progress = 13
    week = last_week

    while week < weeks_in_progress:

        week += 1
        weeks_left = weeks_in_progress - week

        weekly_expenses = checking_for_float("How much money did you spend this week? ")

        weekly_spending_list.append(weekly_expenses)
        week_numbers.append(week)

        money_available -= weekly_expenses

        append_to_csv(week, weekly_expenses, money_available)

        question = "Do you want to continue? [yes/no] "
        if money_available > 0:
            print(f"You have ${money_available:.2f} for the next {weeks_left} weeks.")
            cont = ask_continue(question)
            if not cont:
                break

        elif money_available == 0:
            print("You have used all of your available money.")
            print(f"Spending any more will cause you to fall below your savings goal of ${finish}.")
            cont = ask_continue(question)
            if not cont:
                break

        else:
            print("You have spent more money than you planned.")
            print(f"You are ${abs(money_available):.2f} below your savings goal of ${finish:.2f}. "
                  f"You still have {weeks_left} weeks remaining.")
            if not ask_continue(question):
                break

    return money_available, weekly_spending_list, week_numbers

"""
SUMMARY  ---------------------------------------------------------------------------------------
"""

def summary(start, finish, weekly_spending_list, week_numbers, total_spent, money_available):
    print("SUMMARY ---------------------------------------------------")
    print(f"You started with ${start:.2f}.")
    print(f"You had a goal of saving ${finish:.2f}.")

    money_spent = sum(weekly_spending_list)
    print(f"You have spent ${money_spent:.2f}.")

    money_left = start - money_spent
    print(f"You now have ${money_left:.2f}.")

    if money_left > finish:
        comparison = "you spent less than you planned."
        success = "successful"
    elif money_left == finish:
        comparison = "you spent exactly as much as you planned."
        success = "successful"
    else:
        comparison = "you spent more than you planned."
        success = "not successful"

    print(f"This means {comparison}")
    print(f"So, you were {success} in achieving your savings goal.")

    desired_stats = ask_continue("Would you like to view your summary statistics? [yes/no] ")
    if desired_stats:
        print("SUMMARY STATISTICS ----------------------------------------")
        avg_wkly = avg_spending(weekly_spending_list)
        print(f"Your average weekly spending was: ${avg_wkly:.2f}")
        on_track(start, finish, avg_wkly, weekly_spending_list)

    desired_visuals = ask_continue("Would you like to view your graph statistics? [yes/no] ")
    if desired_visuals:
        bar_chart(week_numbers, weekly_spending_list)
        pie_chart(total_spent, money_available, weekly_spending_list)


"""
SUMMARY STATISTICS  ----------------------------------------------------------------------------
"""

def avg_spending(weekly_spending_list):
    total_spent = sum(weekly_spending_list)
    total_weeks = len(weekly_spending_list)
    avg_wkly_spending = total_spent / total_weeks
    return avg_wkly_spending


def on_track(start, finish, avg_wkly_spending, weekly_spending_list):
    weeks = 13
    spending_amt_allowed = start - finish
    weeks_passed = len(weekly_spending_list)
    amount_spent_so_far = sum(weekly_spending_list)
    weeks_remaining = weeks - weeks_passed

    necessary_avg = spending_amt_allowed / weeks
    print(f"You needed to spend an average of ${necessary_avg:.2f} per week to meet your savings goal.")

    if avg_wkly_spending <= necessary_avg:
        print("You are on track to meet your savings goal.")
    else:
        print("You are not on track to meet your savings goal.")

        if amount_spent_so_far > spending_amt_allowed:
            print("You have already spent too much to meet your goal.")
            return

        adjusted_budget = (spending_amt_allowed - amount_spent_so_far) / weeks_remaining
        print(f"To get back on track, your new average weekly spending should be ${adjusted_budget:.2f}")


"""
VISUALIZATION --------------------------------------------------------------------------------
"""

def bar_chart(week_numbers, weekly_spending_list):
    n = len(weekly_spending_list)
    cmap = plt.get_cmap("Pastel1")
    pastel_colors = cmap(np.linspace(0, 1, n))

    fig, ax = plt.subplots()
    bars = ax.bar(week_numbers, weekly_spending_list, color=pastel_colors, edgecolor='black', linewidth=1)

    for bar, amount in zip(bars, weekly_spending_list):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"${amount:.2f}",
            ha='center', va='bottom', fontsize=10
        )

    ax.set_xticks(week_numbers)
    ax.set_xlabel("Week")
    ax.set_ylabel("Spending (dollars)")
    ax.set_title("Weekly Spending")
    plt.show()


def pie_chart(total_spent, money_available, weekly_spending_list):
    """
    Draw a pie chart of weekly spending and remaining or overspent money.
    Pastel1 colors are used for weekly slices, gray for remaining, red for overspent.
    Dollar amounts are displayed inside slices. Legend shows Week and amount with black outlines.
    """
    n = len(weekly_spending_list)
    cmap = plt.get_cmap("Pastel1")
    pastel_colors = cmap(np.linspace(0, 1, n))

    values = weekly_spending_list.copy()
    labels = [f"Week {i+1}" for i in range(n)]
    colors = list(pastel_colors)
    explode = [0] * n

    if money_available >= 0:
        values.append(money_available)
        labels.append("Remaining")
        colors.append("gray")
        explode.append(0)
        title_text = "Spending Breakdown (Total Spendable Money)"
    else:
        overspent = abs(money_available)
        values.append(overspent)
        labels.append("Overspent")
        colors.append("red")
        explode.append(0.1)
        title_text = f"Spending Breakdown – Overspent ${overspent:.2f}!"

    plt.figure(figsize=(7, 7))

    def dollar_autopct(pct, allvals):
        absolute = pct / 100 * sum(allvals)
        return f"${absolute:.2f}"

    patches, texts, autotexts = plt.pie(
        values,
        labels=None,
        colors=colors,
        autopct=lambda pct: dollar_autopct(pct, values),
        startangle=90,
        explode=explode,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 10}
    )

    from matplotlib.patches import Patch
    legend_patches = [Patch(facecolor=colors[i], edgecolor='black', linewidth=1) for i in range(len(colors))]
    legend_labels = [f"{labels[i]}: ${values[i]:.2f}" for i in range(len(values))]

    plt.legend(
        legend_patches,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        title="Spending Breakdown"
    )

    plt.title(title_text)
    plt.tight_layout()
    plt.show()


"""
FLASK INTEGRATION  -----------------------------------------------------------------------------
"""

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


"""
MAIN FUNCTION -------------------------------------------------------------------------------
"""

def main():
    create_csv_if_not_exists()
    total_spent, last_week, weekly_spending_list, week_numbers, starting_money, finishing_money = read_csv()

    if starting_money is None or finishing_money is None:
        starting_money = checking_for_float("How much money do you have to start with? (Enter amount in USD) ")
        finishing_money = checking_for_smaller_num(starting_money, "How much money do you want to save? ")
        update_start_finish_csv(starting_money, finishing_money)

    money_available, weekly_spending_lst, week_numbers = money_tracker(starting_money, finishing_money, total_spent, last_week, weekly_spending_list, week_numbers)

    summary(starting_money, finishing_money, weekly_spending_list, week_numbers, total_spent, money_available)


# main()