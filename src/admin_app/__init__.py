from flask import Flask
from .views import admin_blueprint
from .config import APP_SECRET_KEY

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.register_blueprint(admin_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
