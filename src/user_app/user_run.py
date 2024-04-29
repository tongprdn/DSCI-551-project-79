from flask import Flask, url_for
from views import user_blueprint
from config import APP_SECRET_KEY

app = Flask(__name__, template_folder='template', static_folder='static')
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.register_blueprint(user_blueprint)


@app.template_filter('smart_truncate')
def smart_truncate(content, length=100):
    if isinstance(content, list):
        content = ', '.join(map(str, content))
    if isinstance(content, (int, float)):
        content = str(content)
    if isinstance(content, str):
        return content if len(content) <= length else content[:length] + '...'
    return content


# Or using the method
app.add_template_filter(smart_truncate, 'smart_truncate')

if __name__ == '__main__':
    app.run(debug=True)
