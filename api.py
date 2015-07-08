# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 09:54:17 2015

@author: jerelyn
"""
from flask import Flask, jsonify, render_template, flash, request, \
    session, redirect, url_for, g 
from flask_restful import Api, Resource, abort
import json
import os
from operator import itemgetter

#creating application
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='smart'
))
app.config.from_envvar('EVENT_SETTINGS', silent=True)

#extending application to api
api = Api(app)


with open('data/90_ncr_dummy_hour.json') as data_file:
	data = json.load(data_file)


def abort_index_exceed(cls_id):
    ncls = max(data, key=itemgetter('cls'))['cls']
    if cls_id > ncls:
        abort(404, message="cls input exceeded max cls_id")

#Api classes returning json
class Data(Resource):
    def get(self):
        return data
api.add_resource(Data, '/api/data')

class Entry(Resource):
    def get(self,cls_id):
        abort_index_exceed(cls_id)
        return data[cls_id]
api.add_resource(Entry, '/api/data/<int:cls_id>')

#Flask-frontend navigation
@app.route('/') #homepage
def home():
    return render_template('layout.html')

@app.route('/map', methods=['GET', 'POST']) #homepage
def map():
    error = None
    datum = {}
    lat = 0
    lon = 0
    cls = 0
    if request.method == 'POST':
        if request.form['cluster'] == "":
            flash('Please enter a valid cluster value')
        else:
            datum = data[int(request.form['cluster'])]
            lat = datum['lat']
            lon = datum['lon']
            cls = datum['cls']
            flash('Data for cluster:  ' + str(cls))
    return render_template('map.html', entry=datum, lat=lat, lon=lon)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('map'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    
    




