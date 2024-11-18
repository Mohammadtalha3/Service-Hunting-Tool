from flask import Flask
from flask_login import LoginManager
from Model.db_models import db, User,init_app
#from Model.db_models import User, init_app
from database_conf.db_config import Config

try:
    from Model.db_models import db, User, init_app  # Import db, User model, and init_app function from models package
except ImportError as e:
    print(f"Error importing models: {e}")
    raise

import os
import sys
import os
print(f"Current working directory: {os.getcwd()}")


sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
app.config.from_object(Config)  # Assuming you have a Config class for configuration

init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



from Routes.routes import *
#from routess import *

# Import routes and continue with app setup as usual

if __name__ == '__main__':
    app.run(debug=True)