from app import create_app, db

# 🔥 VERY IMPORTANT: import all models
from app.models.user import User
from app.models.expense import Expense
from app.models.budget import Budget

app = create_app()

with app.app_context():
    print("DB PATH =>", app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()
    print("✅ Tables created")
