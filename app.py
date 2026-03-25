from flask import Flask, render_template, request, redirect, url_for
from savings_made_simple import (
    create_csv_if_not_exists, read_csv, update_start_finish_csv,
    append_to_csv, calculate_week, get_summary
)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)
FILENAME = "savings_made_simple.csv"

# -----------------------
# GLOBAL COLOR PALETTE (same for pie + bar)
# -----------------------
COLORS = [
    '#6c63ff',  # purple (primary)
    '#00d4ff',  # cyan
    '#ff6b9d',  # pink
    '#00ff88',  # green
    '#ffb347',  # orange
    '#ff4d4d',  # red
    '#a78bfa',  # lavender
    '#34d399',  # mint
    '#f59e0b',  # amber
    '#60a5fa',  # blue
]


# -----------------------
# BAR CHART
# -----------------------
def plot_bar_chart(weeks, amounts):
    fig, ax = plt.subplots()

    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#111111')

    bar_colors = COLORS[:len(weeks)]
    ax.bar(weeks, amounts, color=bar_colors)

    ax.set_xticks(range(1, len(weeks) + 1))
    ax.set_xlabel("Week", color='#888888')
    ax.set_ylabel("Amount Spent", color='#888888')
    ax.set_title("Weekly Spending", color='#ffffff')
    ax.tick_params(colors='#888888')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')

    buffer = BytesIO()
    plt.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close(fig)
    return image


# -----------------------
# PIE CHART
# -----------------------
def plot_pie_chart(weekly_spending_list, money_left):
    values = weekly_spending_list.copy()
    labels = [f"Week {i+1}" for i in range(len(weekly_spending_list))]

    # Same shared colors
    colors = COLORS[:len(values)]

    if money_left >= 0:
        values.append(money_left)
        labels.append("Remaining")
        colors.append("gray")
    else:
        overspent = abs(money_left)
        values.append(overspent)
        labels.append("Overspent")
        colors.append("red")

    fig, ax = plt.subplots()

    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')

    ax.pie(
        values,
        labels=None,
        autopct=lambda pct: f"${pct/100*sum(values):.2f}",
        startangle=90,
        colors=colors,
        textprops={'color': '#ffffff'}
    )

    ax.set_title("Spending Breakdown", color='#ffffff')

    buffer = BytesIO()
    plt.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close(fig)
    return image


# -----------------------
# MAIN ROUTE
# -----------------------
create_csv_if_not_exists()

@app.route("/", methods=["GET", "POST"])
def index():
    total_spent, last_week, weekly_spending_list, week_numbers, starting_money, finishing_money = read_csv(FILENAME)

    bar_chart_img = None
    pie_chart_img = None

    if request.method == "POST":
        action = request.form.get("action")

        # First-time setup
        if not starting_money or not finishing_money:
            start_str = request.form.get("start")
            finish_str = request.form.get("finish")
            if start_str and finish_str:
                starting_money = float(start_str)
                finishing_money = float(finish_str)
                update_start_finish_csv(starting_money, finishing_money)

        # Log a new week of spending
        elif action == "submit_week":
            weekly_expense_str = request.form.get("weekly_expense")
            if weekly_expense_str:
                weekly_expense = float(weekly_expense_str)
                week_number = last_week + 1
                money_available, weekly_spending_list = calculate_week(
                    starting_money, finishing_money, weekly_spending_list,
                    week_number, weekly_expense
                )
                append_to_csv(week_number, weekly_expense, money_available, FILENAME)
                last_week = week_number

        # Exit
        elif action == "exit_now":
            return redirect(url_for("index"))

        # Reset all data
        elif action == "start_over":
            with open(FILENAME, "w", newline="") as f:
                f.write("StartMoney,FinishMoney\n")
                f.write(",\n")
                f.write("Week,MoneySpent,RemainingBudget\n")
            return redirect(url_for("index"))

        return redirect(url_for("index"))

    # Prepare summary
    summary = get_summary(starting_money or 0, finishing_money or 0, weekly_spending_list)

    # Generate charts
    if weekly_spending_list:
        bar_chart_img = plot_bar_chart(
            list(range(1, len(weekly_spending_list) + 1)),
            weekly_spending_list
        )
        pie_chart_img = plot_pie_chart(
            weekly_spending_list,
            summary["money_left"]
        )

    return render_template(
        "index.html",
        starting_money=starting_money,
        finishing_money=finishing_money,
        week_number=last_week + 1,
        weekly_spending_list=weekly_spending_list,
        summary=summary,
        bar_chart_img=bar_chart_img,
        pie_chart_img=pie_chart_img
    )


# -----------------------
# RUN APP
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5500)