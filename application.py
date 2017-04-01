from flask import Flask
from flask import render_template
from flask.ext.babel import Babel
from flask import request

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['fi', 'en'])

@app.route('/')
def index():
    print app.config['BABEL_DEFAULT_LOCALE']
    # return "Hello"
    return render_template('index.html')