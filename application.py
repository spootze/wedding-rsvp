from os import environ

from flask import Flask
from flask import render_template
from flask.ext.babel import Babel, gettext
from flask import request, redirect, jsonify

import json

from database import Database
from models import Registration, Gift, GiftRegistration

from sqlalchemy.sql import func

application = Flask(__name__)

application.config.from_object('config.BaseConfig')
if 'RSVP_CONFIG' in environ:
  application.config.from_envvar('RSVP_CONFIG')


db = Database(application)
db.init_db()

babel = Babel(application)


@babel.localeselector
def get_locale():
    url_lang_candidate = request.path[1:].split('/', 1)[0]
    if url_lang_candidate in ['fi', 'en']:
      return url_lang_candidate
    else:
      return request.accept_languages.best_match(['fi', 'en'])

@application.route('/')
@application.route('/fi')
@application.route('/en')
def index():
    return render_template('index.html', gifts=Gift.query.all(), remaining_counts=get_remaining_counts())

@application.route('/create_gift')
def create_gift():
    g = Gift('Megapaavo', 'https://www.paavovayrynen.fi/', 50)
    db.db_session.add(g)
    db.db_session.commit()

@application.route('/register_gift', methods=['POST'])
def register_gift():

  try:
    gift_id = request.form['gift_id']
    count = request.form['count']

    if get_remaining_count(gift_id) < count:
      raise Exception('Attempting to over-reserve gift.')

    gf = GiftRegistration(gift_id, count)
    db.db_session.add(gf)
    db.db_session.commit()

    return jsonify({
      'success':True,
      'message':gettext('Thank you! Your gift reservation has been successfully recorded!'),
      'data': request.form  
    })

  except Exception as e:
    application.logger.error(e)

    message = gettext('Unfortunately there was an error in processing your reservation')

    db.db_session.rollback()

    return jsonify({
      'success':False,
      'message': message,
      'data': request.form
    })

  return json.dumps(request.form)




@application.route('/rsvp', methods=['POST'])
def add_registration():

  try:
    r = Registration(
      request.form['name'],
      request.form['email'],
      int(request.form['count']),
      request.form['info']
    )
    db.db_session.add(r)
    db.db_session.commit()
    return jsonify({
      'success':True,
      'message':gettext('Thank you! Your RSVP has been successfully recorded!'),
      'data': request.form  
    })

  except Exception as e:
    application.logger.error(e)

    message = gettext('Unfortunately there was an error in processing your reservation')

    if str(e).find('UNIQUE constraint failed') > -1 or str(e).find('value violates unique constraint') > -1:
      message = gettext("""Unfortunately it seems that either the name or email has
                   already been used to RSVP""")



    db.db_session.rollback()

    return jsonify({
      'success':False,
      'message': message,
      'data': request.form
    })

  return json.dumps(request.form)

def get_remaining_counts():
  gifts = Gift.query.all()
  remaining_counts = {}
  for gift in gifts:
    remaining_counts[gift.id] = get_remaining_count(gift.id)
  return remaining_counts

def get_remaining_count(gift_id):
  initial_count = Gift.query.get(gift_id).initial_count
  q = db.db_session.query(func.sum(GiftRegistration.count))
  registrations = q.filter(GiftRegistration.gift_id == gift_id).scalar() or 0
  return initial_count - registrations

if __name__ == "__main__":
  application.debug = True
  application.run()
