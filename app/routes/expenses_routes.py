from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.expense import Expense
from app import db
from datetime import datetime


# 🔹 Blueprint
expense_bp = Blueprint("expense", __name__)

# ===============================
# ADD EXPENSE
# ===============================


@expense_bp.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        expense = Expense(
            user_id=session["user_id"],
            amount=float(request.form["amount"]),
            category=request.form["category"],
            date=datetime.strptime(
                request.form["date"], "%Y-%m-%d"
            ).date(),
            description=request.form.get("description")
        )

        db.session.add(expense)
        db.session.commit()

        return redirect(url_for("dashboard.dashboard"))

    return render_template("add_expense.html")



# ===============================
# VIEW ALL EXPENSES
# ===============================
@expense_bp.route("/expenses")
def view_expenses():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    expenses = Expense.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Expense.date.desc()).all()

    return render_template("view_expenses.html", expenses=expenses)




