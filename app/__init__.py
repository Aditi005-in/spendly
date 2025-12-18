from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os

db = SQLAlchemy()   

def create_app():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates")
    )

    app.config.from_object(Config)

    db.init_app(app)   # 👈 VERY IMPORTANT
    
    from app.routes.auth_routes import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
 
    from app.routes.expenses_routes import expense_bp
    app.register_blueprint(expense_bp)



    return app


