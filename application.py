from flask import Flask
from flask import render_template
from flask.ext.babel import Babel
from flask import request

application = Flask(__name__)
application.config.from_object('config.BaseConfig')
babel = Babel(application)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['fi', 'en'])

@application.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
  application.debug = True
  application.run()
