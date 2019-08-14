import sys

from base64 import b64encode
from werkzeug.security import generate_password_hash, check_password_hash

from flask import render_template
from flask import request, redirect, url_for
from flask import jsonify

from app import app
from app import task_queue
from app import db
from app import auth
from app.models import Donation

from config import Config

@auth.verify_password
def verify_password(username, password):
    if username == Config.BASIC_AUTH_USERNAME:
        return check_password_hash(generate_password_hash(Config.BASIC_AUTH_PASSWORD), password)
    else:
        return False

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    username = request.json['username']
    password = request.json['password']

    if verify_password(username, password):
        return "Ok"
    else:
        return "Error", 401

@app.route('/api/donations')
def index():
    page = request.args.get('page', 1, type=int)
    amount_filter = request.args.get('amount_filter', False)
    only_blank  = request.args.get('only_blank', False)

    donations = Donation \
                .query \
                .order_by(Donation.vod_published_at.asc(), Donation.donated_at.asc()) \

    if amount_filter:
        donations = donations.filter(Donation.amount >= amount_filter)
    if only_blank:
        donations = donations.filter(Donation.amount == None)

    donations = donations.paginate(page, 50, False)

    return jsonify(json=[i.serialize for i in donations.items])

@app.route('/api/donations', methods=['POST'])
@auth.login_required
def update():
    donation = Donation.query.get(request.form['id'])
    donation.approved = True

    if request.form['author']:
        donation.author = request.form['author']

    if request.form['amount']:
        donation.amount = request.form['amount']

    if request.form['currency']:
        donation.currency = request.form['currency']

    db.session.commit()

    return jsonify(donation.serialize)

@app.route('/api/donations/delete', methods=['POST'])
@auth.login_required
def delete():
    donation = Donation.query.get(request.form['id'])

    db.session.delete(donation)
    db.session.commit()

    return jsonify(donation.serialize)

@app.route('/api/recognize')
@auth.login_required
def recognize():
    job = task_queue.enqueue('app.jobs.recognize_donations', job_timeout=10000000)

    return f"Enqueued {job.id}"

@app.route('/api/re_recognize')
@auth.login_required
def re_recognize():
    job = task_queue.enqueue('app.jobs.re_recognize_donations', job_timeout=10000000)

    return f"Enqueued {job.id}"
