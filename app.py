import psycopg2
import os

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = os.getenv('food_lookup_key')

@app.route('/')
def foodlookup():
    return render_template('foodlookup.html')

@app.route('/add_food', methods=['GET', 'POST'])
def addfood():
    if request.method == 'POST':
        try:
            # Extract data from form
            food_name = request.form['foodName']
            portion_size = request.form['portion_size']
            calories = request.form['calories']
            total_fat = request.form['total_fat']
            saturated_fat = request.form['saturated_fat']
            trans_fat = request.form['trans_fat']
            cholesterol = request.form['cholesterol']
            sodium = request.form['sodium']
            total_carbohydrates = request.form['total_carbohydrates']
            sugars = request.form['sugars']
            protein = request.form['protein']
            vitamin_d = request.form['vitamin_d']
            calcium = request.form['calcium']
            iron = request.form['iron']
            potassium = request.form['potassium']

            # Validate data (server-side validation)
            if not food_name:
                raise ValueError("Must specify food name")
            if not food_name.isalpha():
                raise ValueError("Invalid food name")
                
            # Convert empty strings to None and strings to appropriate types
            def convert_or_none(value):
                return float(value) if value.replace('.', '', 1).isdigit() else None

            # Validate other fields
            if not convert_or_none(portion_size):
                raise ValueError("Portion size must be a real number or empty")
            if not convert_or_none(calories):
                raise ValueError("Calories must be a real number or empty")
            if not convert_or_none(total_fat):
                raise ValueError("Total fat must be a real number or empty")
            if not convert_or_none(saturated_fat):
                raise ValueError("Saturated fat must be a real number or empty")
            if not convert_or_none(trans_fat):
                raise ValueError("Trans fat must be a real number or empty")
            if not convert_or_none(cholesterol):
                raise ValueError("Cholesterol must be a real number or empty")
            if not convert_or_none(sodium):
                raise ValueError("Sodium must be a real number or empty")
            if not convert_or_none(total_carbohydrates):
                raise ValueError("Total Carbohydrates must be a real number or empty")
            if not convert_or_none(sugars):
                raise ValueError("Sugars must be a real number or empty")
            if not convert_or_none(protein):
                raise ValueError("Protein must be a real number or empty")
            if not convert_or_none(vitamin_d):
                raise ValueError("Vitamin D must be a real number or empty")
            if not convert_or_none(calcium):
                raise ValueError("Calcium must be a real number or empty")
            if not convert_or_none(iron):
                raise ValueError("Iron must be a real number or empty")
            if not convert_or_none(potassium):
                raise ValueError("Potassium must be a real number or empty")
            
            # Insert into database
            conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
            cur = conn.cursor()
            query = """
                INSERT INTO Foods (name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, sugars, protein, vitamin_d, calcium, iron, potassium) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (food_name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, sugars, protein, vitamin_d, calcium, iron, potassium))
            conn.commit()
            cur.close()
            conn.close()

            flash('Food item added successfully!')
            return redirect(url_for('addfood'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('addfood'))

    return render_template('addfood.html')

@app.route('/db_test')
def testing():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    conn.close()
    return "Database Connection Successful!"

@app.route('/db_create')
def create():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Foods (
        food_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        
        portion_size REAL,           -- Usually in grams (g)
        calories REAL,               -- Usually in kcal
        total_fat REAL,              -- Typically in grams (g)
        saturated_fat REAL,          -- Typically in grams (g)
        trans_fat REAL,              -- Typically in grams (g)
        cholesterol REAL,            -- Typically in milligrams (mg)
        sodium REAL,                 -- Typically in milligrams (mg)
        total_carbohydrates REAL,    -- Typically in grams (g)
        dietary_fiber REAL,          -- Typically in grams (g)
        sugars REAL,                 -- Typically in grams (g)
        protein REAL,                -- Typically in grams (g)
        vitamin_d REAL,              -- Usually in micrograms (µg) or IU
        calcium REAL,                -- Typically in milligrams (mg)
        iron REAL,                   -- Typically in milligrams (mg)
        potassium REAL               -- Typically in milligrams (mg)
        );
    ''')
    conn.commit()
    conn.close()
    return "Foods Table Successfully Created!"

@app.route('/db_insert')
def inserting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    food_items = [('Avocado', 230, 384, 35, 4.9, None, None, 18, 20, 16, 0.7, 4.5, 0, 30, 1.4, 1166),
                  ('Onion, raw', 160, 64, 0.2, 0.1, None, None, 6.4, 15, 2.7, 6.8, 1.8, 0, 37, 0.3, 234),
                  ('Salami', 28, 119, 10, 3.7, None, 22, 529, 0.3, 0, 0.3, 6.1, None, 2.8, 0.4, 95)]
    cur.executemany('INSERT INTO Foods (name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, vitamin_d, calcium, iron, potassium) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', food_items)
    conn.commit()
    conn.close()
    return "Foods Table Successfully Populated!"

@app.route('/db_select')
def selecting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM Foods;
        ''')
    records = cur.fetchall()
    conn.close()
    response_string=""
    response_string+="<table>"
    for food in records:
        response_string+="<tr>"
        for info in food: 
            response_string+="<td>{}</td>".format(info)
        response_string+="</tr>"
    response_string+="</table>"
    return response_string
    
@app.route('/db_drop')
def dropping():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    cur.execute('''
        DROP TABLE Foods;
    ''')
    conn.commit()
    conn.close()
    return "Foods Table Successfully Dropped"