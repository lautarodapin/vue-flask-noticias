from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import api_bp
from database import db_session
from config import config

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(api_bp)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



# migrate = Migrate(app, db_session)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    app.run(debug=True)