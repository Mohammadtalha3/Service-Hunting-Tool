from app import app, db
from models import User, SearchKeyword, Listing, UserSearch

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
