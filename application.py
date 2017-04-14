from os import environ

from flask import Flask
from flask import render_template
from flask.ext.babel import Babel
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
    return request.accept_languages.best_match(['fi', 'en'])

@application.route('/')
def index():
    return render_template('index.html', gifts=get_gifts())

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

    gf = GiftRegistration(gift_id, count)
    db.db_session.add(gf)
    db.db_session.commit()

    return jsonify({
      'success':True,
      'message':'Thank you! Your gift reservation has been successfully recorded!',
      'data': request.form  
    })

  except Exception as e:
    application.logger.error(e)

    message = 'Unfortunately there was an error in processing your reservation'

    db.db_session.rollback()

    return jsonify({
      'success':False,
      'message': message,
      'data': request.form,
      'exception': str(e)
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
    # TODO: localization
    return jsonify({
      'success':True,
      'message':'Thank you! Your RSVP has been successfully recorded!',
      'data': request.form  
    })

  except Exception as e:
    application.logger.error(e)

    message = 'Unfortunately there was an error in processing your reservation'

    if str(e).find('UNIQUE constraint failed') > -1 or str(e).find('value violates unique constraint') > -1:
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

# TODO: join giftregistration for already registered count
def get_gifts():
  gifts = Gift.query.all()
  for gift in gifts:
    registrations = db.db_session.query(func.sum(GiftRegistration.count)).filter(GiftRegistration.gift_id == gift.id).scalar()
    gift.remaining_count = gift.initial_count
    if registrations is not None:
      gift.remaining_count -= registrations

  return gifts

def get_gift(gift_id):
  return db.db_session.query(Gift).get(gift_id)

if __name__ == "__main__":
  application.debug = True
  application.run()
