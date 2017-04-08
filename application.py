from os import environ

from flask import Flask
from flask import render_template
from flask.ext.babel import Babel
from flask import request, redirect, jsonify

import json

from database import Database
from models import Registration

application = Flask(__name__)

application.config.from_object('config.BaseConfig')
if 'RSVP_CONFIG' in environ:
  application.config.from_envvar('RSVP_CONFIG')


db = Database(application)
db.init_db()

babel = Babel(application)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['fi', 'en'])

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/rsvp', methods=['POST'])
def add_registration():

  try:
    r = Registration(
      request.form['name'],
      request.form['email'],
      int(request.form['count'])
    )
    db.db_session.add(r)
    db.db_session.commit()
    # TODO: localization
    return jsonify({
      'success':True,
      'message':'Thank you! Your RSVP has been successfully recorded!',
      'data': request.form  
    })

  except Exception as e:
    application.logger.error(e)

    message = 'Unfortunately there was an error in processing your reservation'

    if str(e).find('UNIQUE constraint failed') > -1:
      # TODO: localization
      message = """Unfortunately it seems that either the name or email has
                   already been used to RSVP"""

    db.db_session.rollback()

    return jsonify({
      'success':False,
      'message': message,
      'data': request.form,
      'exception': str(e)
    })

  return json.dumps(request.form)

def get_registrations():
  return Registration.query.all()

if __name__ == "__main__":
  application.debug = True
  application.run()
