from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_user(first_name, last_name, email, password):
    if User.query.filter_by(email=email).first():
        return False

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()
    return True


