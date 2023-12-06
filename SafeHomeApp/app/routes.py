from app import app
from app import database as db_helper
from flask import Flask, request, render_template, redirect, url_for, session, flash, render_template_string, jsonify
from datetime import time
import folium
import requests
from app import map
import json

@app.route('/')
def index_page():
    if 'email' in session:
        return redirect(url_for('homepage'))
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Check if the user is already logged in
        if 'email' in session:
            return redirect(url_for('homepage'))
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate the credentials
        if db_helper.user_validation(email, password):
            # set up the session
            user_info = db_helper.get_user_info(email)
            session['username'] = user_info[0]
            session['email'] = user_info[1]
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html', error='Invalid username or password')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('index_page'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # Check if the user is already logged in
        if 'email' in session:
            return redirect(url_for('homepage'))
        return render_template('signup.html')
    elif request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        gender = request.form['Gender']
        age = request.form['Age']
        try:
            db_helper.user_signup(email, password, gender, age)
            flash('Account created successfully, please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred:' + str(e), 'error')
            return render_template('signup.html')


@app.route('/home')
def homepage():
    if 'email' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

@app.route('/search')
def search():
    if 'email' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    else:
        return render_template('search.html')

@app.route('/trends')
def trends():
    if 'email' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    else:
        return render_template('trends.html')
    

def geocoding_api(address):
    # 替换为你的API密钥
    api_key = "AIzaSyA5HacO7Des_9mvjxT1ZASj61Awk88JI_g"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return None, None  # 或者处理错误
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return None, None  # 地址无法解析


@app.route('/submit_report', methods=['GET', 'POST'])
def submit_report():
    if request.method == 'GET':
        return 1  # You might want to return a proper HTML response here
    elif request.method == 'POST':
        # get the lat and lng from the address
        location_name = request.form['LocationId'] + ' Los Angeles'
        lat, lng = geocoding_api(location_name)
        if lat is None or lng is None:
            flash('Geocoding failed.', 'error')
            return render_template('report.html')
        # get the crime type
        crime_id = int(request.form['CrimeType'])
        # get the crime date
        crime_date = request.form['Date']  # Updated to match the HTML form field name
        # get the crime time
        time_str = request.form['Time']
        hour, minute = map(int, time_str.split(':'))
        crime_time_ = time(hour, minute, 0)
        minute = crime_time_.hour  # 某个分钟值
        second = crime_time_.minute # 某个秒值
        crime_time = time(0, minute, second)

        PremisID = int(request.form['LocationType'])
        #--------------------测试输出--------------------------------------------------------------------------
        flash_message = f"Latitude: {lat}, Longitude: {lng}, Location ID: {location_name}, Crime ID: {crime_id}, Date: {crime_date}, Time: {crime_time}, PremisID: {PremisID}"
        flash(flash_message, 'success')
        #-------------------------------------------------------------------------------------------------------
        
        try:
            db_helper.report_submit(lat, lng, location_name, crime_id, crime_date, crime_time, PremisID)
            flash('Report submitted successfully.', 'success')
            return redirect(url_for('report'))
        except Exception as e:
            flash('An error occurred:' + str(e), 'error')
            return render_template('report.html')


@app.route('/report')
def report():
    if 'email' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('report.html')
        elif request.method == 'POST':
            return render_template('report.html')


@app.route('/get_map',methods=['POST'])
def get_map():
    input1 = request.form.get('input1')
    input2 = request.form.get('input2')
    origin = geocoding_api(input1)
    destination = geocoding_api(input2)
    m = map.get_route(origin, destination)
    # set the iframe width and height
    m.get_root().width = "1000px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()
    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )

@app.route('/get_map_default')
def get_map_default():
    m = folium.Map(location=[34.0522, -118.2437], zoom_start=10)
    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )

@app.route('/get_heatmap',methods=['GET'])
def get_heatmap():
    results = db_helper.get_trends()
    m = map.get_heatmap(results)
    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()
    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )

@app.route('/like_destination', methods=['POST'])
def like_destination():
    destination = request.form.get('destination')
    # Get the userid from the session
    userid = session['username']
    # Save the destination to the database
    db_helper.like_destination(userid, destination)
    return 'success'

@app.route('/get_favourite_locations', methods=['GET'])
def get_favourite_locations():
    userid = session['username']
    locations = db_helper.get_favourite_locations(userid)
    return jsonify(locations)

@app.route('/delete_favourite_location', methods=['POST'])
def delete_favourite_location():
    location = request.form.get('location')
    userid = session['username']
    db_helper.delete_location(userid, location)
    return 'success'

@app.route('/update_favourite_location', methods=['POST'])
def update_favourite_location():
    location = request.form.get('location')
    new_location = request.form.get('new_location')
    userid = session['username']
    db_helper.update_location(userid, location, new_location)
    return 'success'

@app.route('/search_crime', methods=['POST'])
def search_crime():
    crime_type = request.form.get('crime_type')
    area = request.form.get('area')
    events = db_helper.search_crimeEvents(crime_type, area)
    data = [(crime, location, date.strftime('%Y-%m-%d %H:%M:%S')) for crime, location, date in events]
    json_return = json.dumps(data)
    return json_return

@app.route('/run_update', methods=['GET'])
def run_update():
    db_helper.call_stored_procedure()
    return 'success'