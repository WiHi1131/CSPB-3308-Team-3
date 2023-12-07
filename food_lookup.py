###############################################################################
## This is starter code for the Calorie/Food Lookup page of Team 3's Software 
## Development project for CSPB 3308. 
##
## Description:
##    This module provides functionality for users to look up the calorie and nutritional values of various foods.
##    Users can search for common foods from a predefined database or input custom values for foods not already listed.
##    Results are displayed, allowing users to track and monitor their daily intake effectively.

##Features:
##    - User input field for food name search.
##    - Auto-populate functionality linked to a relational database.
##    - Measurement and unit of measurement input options.
##    - Basic calculation to compute calories based on user input.
##    - Error handling to address invalid inputs or database errors.
##    - Input validation to ensure the data's accuracy and integrity.
##    - Connection to a relational database for fetching food data.
##    - Stylish UI with images and clear typography for ease of use.
##    - Hyperlinks to other related pages for a seamless user journey.
##    - Output display including the current entry, daily totals, and popular food choices.

## Author: William Hinkley - October 2023
##
###############################################################################


###############################################################################
import prefix
import os
import json
import psycopg2

from flask import Flask, url_for
from markupsafe import escape
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from data_insertion import addFood
from models import db, Food

# create app to use in this Flask application
app = Flask(__name__)

# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine
prefix.use_PrefixMiddleware(app)   

# Setup Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db') # Path to your SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: This disables a warning about a Flask-SQLAlchemy feature that you probably won't use.

db.init_app(app)

# test route to show prefix settings
@app.route('/prefix_url')  
def prefix_url():
    return 'The URL for this page is {}'.format(url_for('prefix_url'))

@app.route('/foodlookup', methods=['GET', 'POST'])
def foodtracker():
    return render_template('foodlookup.html')

@app.route('/search_food', methods=['GET'])
def search_food():
    query = request.args.get('query')
    print(f"Query received: {query}")  # Debug print
    if not query:
        return json.dumps([])

    matching_foods = db.session.query(Food).filter(Food.name.like(f"%{query}%")).all()
    print(f"Matching foods from database: {matching_foods}")  # Debug print

    food_names = [food.name for food in matching_foods]
    return json.dumps(food_names)

@app.route('/add_food', methods=['POST'])
def add_food():
    try:
        addFood(
            session=db.session,
            name=request.form['name'],
            portion_size=float(request.form['portion_size']) if request.form['portion_size'] else None,
            calories=float(request.form['calories']) if request.form['calories'] else None,
            total_fat=float(request.form['total_fat']) if request.form['total_fat'] else None,
            saturated_fat=float(request.form['saturated_fat']) if request.form['saturated_fat'] else None,
            trans_fat=float(request.form['trans_fat']) if request.form['trans_fat'] else None,
            cholesterol=float(request.form['cholesterol']) if request.form['cholesterol'] else None,
            sodium=float(request.form['sodium']) if request.form['sodium'] else None,
            total_carbohydrates=float(request.form['total_carbohydrates']) if request.form['total_carbohydrates'] else None,
            dietary_fiber=float(request.form['dietary_fiber']) if request.form['dietary_fiber'] else None,
            sugars=float(request.form['sugars']) if request.form['sugars'] else None,
            protein=float(request.form['protein']) if request.form['protein'] else None,
            vitamin_d=float(request.form['vitamin_d']) if request.form['vitamin_d'] else None,
            calcium=float(request.form['calcium']) if request.form['calcium'] else None,
            iron=float(request.form['iron']) if request.form['iron'] else None,
            potassium=float(request.form['potassium']) if request.form['potassium'] else None
        )
        
        
        
        return jsonify({'message': 'Food added successfully!'})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
with app.app_context():
    db.create_all()

