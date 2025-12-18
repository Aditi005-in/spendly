from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy import func
from datetime import date

from app.models.expense import Expense
from app.models.budget import Budget
from app import db

dashboard_bp = Blueprint("dashboard", __name__)
@dashboard_bp.route("/dashboard")
def dashboard():
    # -------------------------------
    # AUTH CHECK
    # -------------------------------
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # -------------------------------
    # BASIC DEFAULTS (VERY IMPORTANT)
    # -------------------------------
    total_spent = 0
    today_spent = 0
    weekly_avg = 0
    total_transactions = 0

    category_labels = []
    category_data = []

    trend_labels = []
    trend_data = []

    expenses = []
    is_new_user = True

    budget = None
    budget_spent = 0
    budget_used = 0

    # -------------------------------
    # EXPENSE QUERIES
    # -------------------------------
    expenses = Expense.query.filter_by(user_id=user_id)\
        .order_by(Expense.date.desc())\
        .limit(5)\
        .all()

    total_transactions = Expense.query.filter_by(user_id=user_id).count()

    if total_transactions > 0:
        is_new_user = False

        # Total spent
        total_spent = db.session.query(
            func.coalesce(func.sum(Expense.amount), 0)
        ).filter_by(user_id=user_id).scalar()

        # Today's spent
        today_spent = db.session.query(
            func.coalesce(func.sum(Expense.amount), 0)
        ).filter_by(
            user_id=user_id,
            date=date.today()
        ).scalar()

        # Weekly average
        weekly_avg = round(total_spent / 4)

        # Category chart
        category_rows = db.session.query(
            Expense.category,
            func.sum(Expense.amount)
        ).filter_by(user_id=user_id)\
         .group_by(Expense.category)\
         .all()

        for row in category_rows:
            category_labels.append(row[0])
            category_data.append(float(row[1]))

        # Trend chart (last 6 entries)
        trend_rows = Expense.query.filter_by(user_id=user_id)\
            .order_by(Expense.date)\
            .limit(6)\
            .all()

        for i, row in enumerate(trend_rows, start=1):
            trend_labels.append(str(i))
            trend_data.append(float(row.amount))

    # -------------------------------
    # BUDGET LOGIC
    # -------------------------------
    budget = Budget.query.filter_by(user_id=user_id).first()

    if budget:
        budget_spent = total_spent
        budget_used = int((budget_spent / budget.amount) * 100) if budget.amount > 0 else 0

    # -------------------------------
    # RENDER TEMPLATE
    # -------------------------------
    return render_template(
        "dashboard.html",

        user_name=session.get("email", "User"),

        total_spent=total_spent,
        today_spent=today_spent,
        weekly_avg=weekly_avg,
        total_transactions=total_transactions,

        category_labels=category_labels,
        category_data=category_data,

        trend_labels=trend_labels,
        trend_data=trend_data,

        expenses=expenses,
        is_new_user=is_new_user,

        budget=budget.amount if budget else None,
        budget_spent=budget_spent,
        budget_used=budget_used
    )

