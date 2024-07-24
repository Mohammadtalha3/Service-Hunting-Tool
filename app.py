from flask import Flask
from models import db, User, init_app  # Import db, User model, and init_app function from models.py
from db_config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)  # Assuming you have a Config class for configuration

init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



from routes import *
#from routess import *

# Import routes and continue with app setup as usual

if __name__ == '__main__':
    app.run(debug=True)