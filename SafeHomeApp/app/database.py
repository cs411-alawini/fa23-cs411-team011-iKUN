from app import db

def user_validation(email, password):
    conn = db.connect()
    query = 'SELECT * FROM Users WHERE Email = "{}" AND Password = "{}";'.format(email, password)
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) == 0:
        return False
    else:
        return True
    
def user_signup(email, password, gender, age):
    conn = db.connect()

    # Get the maximum user ID
    query = 'SELECT MAX(UserId) FROM Users;'
    result = conn.execute(query).fetchone()
    max_id = result[0] if result[0] else 'user000'

    # Generate new user ID
    base_id = int(max_id[4:])
    new_id = 'user' + str(base_id + 1).zfill(3)

    # Insert new user
    query = 'INSERT INTO Users (UserId, Email, Password, Gender, Age, Role) VALUES ("{}", "{}", "{}", "{}", {}, "user");'.format(new_id, email, password, gender, age)
    conn.execute(query)
    conn.close()

def get_user_info(email):
    conn = db.connect()
    query = 'SELECT * FROM Users WHERE Email = "{}";'.format(email)
    query_rusults = conn.execute(query).fetchall()
    conn.close()
    if query_rusults:
        return query_rusults[0]
    else:
        return None
    

def report_submit(lat, lng, location_name, crime_id, crime_date, crime_time, PremisID):
    conn = db.connect()
    # first check if the location exists
    query = 'SELECT * FROM Reports JOIN Locations ON Reports.LocationId = Locations.LocationId WHERE Locations.LocationName = "{}" AND Locations.Latitude = {} AND Locations.Longitude = {};'.format(location_name, lat, lng)
    query_results = conn.execute(query).fetchall()
    if len(query_results) == 0:
        # insert new location
        query = 'SELECT MAX(LocationId) FROM Locations;'
        result = conn.execute(query).fetchone()
        max_id = result[0] if result[0] else '10000'
        base_id = int(max_id)
        new_id = str(base_id + 1).zfill(5)
        # insert new report
        query = 'INSERT INTO Reports (LocationId, CrimeId, Date, Time) VALUES ("{}", "{}", "{}", "{}");'.format(new_id, crime_id, crime_date, crime_time)
        conn.execute(query)
        # insert new location
        query = 'INSERT INTO Locations (LocationId, LocationName, Latitude, Longitude, PremisId) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(new_id, location_name, lat, lng, PremisID)
        conn.execute(query)
        # insert new CrimeEvent
        query = 'SELECT MAX(EventID) FROM CrimeEvents;'
        result = conn.execute(query).fetchone()
        Eve_max_id = result[0] if result[0] else '300000000'
        Eve_base_id = int(Eve_max_id)
        Eve_base_id = str(Eve_base_id + 1).zfill(9)
        query = 'INSERT INTO CrimeEvents (EventID, Date, Time, Crimeid, Locationid) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(Eve_base_id, crime_date, crime_time, crime_id, new_id)
        conn.execute(query)
        conn.close()
    else:
        # do nothing
        conn.close()

# class Report(db.Model):
#     lat = db.Column(db.Float)
#     lng = db.Column(db.Float)


def like_destination(userid, locationName):
    conn = db.connect()
    query = 'INSERT INTO Favorites(UserId, LocationName) VALUES ("{}", "{}");'.format(userid, locationName)
    conn.execute(query)
    conn.close()

def get_favourite_locations(userid):
    conn = db.connect()
    query = 'SELECT LocationName FROM Favorites WHERE UserId = "{}";'.format(userid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    return_value = [array[0] for array in query_results]
    return return_value

def delete_location(userid, locationName):
    conn = db.connect()
    query = 'DELETE FROM Favorites WHERE UserId = "{}" AND LocationName = "{}";'.format(userid, locationName)
    conn.execute(query)
    conn.close()

def update_location(userid, locationName, newLocationName):
    conn = db.connect()
    query = 'UPDATE Favorites SET LocationName = "{}" WHERE UserId = "{}" AND LocationName = "{}";'.format(newLocationName, userid, locationName)
    conn.execute(query)
    conn.close()

def within_region(max_log, max_lat, min_log, min_lat):
    conn = db.connect()
    query = 'CALL LocationInRegion("{}", "{}", "{}", "{}");'.format(max_log, max_lat, min_log, min_lat)
    query_result = conn.execute(query).fetchall()
    conn.close()

    return query_result

def search_crimeEvents(crime_type, area):
    conn = db.connect()
    query = 'SELECT CrimeTypes.CrimeName, Locations.LocationName, CrimeEvents.Date FROM Locations JOIN Areas ON Locations.Latitude = Areas.Latitude AND Locations.Longitude = Areas.Longitude natural JOIN CrimeEvents natural JOIN CrimeTypes WHERE CrimeTypes.CrimeName LIKE "%%{}%%" AND Areas.AreaName = "{}" ORDER BY CrimeEvents.Date DESC LIMIT 10;'.format(crime_type, area)
    query_result = conn.execute(query).fetchall()
    conn.close()
    return query_result

def call_stored_procedure():
    conn = db.connect()
    query = 'CALL `AnalyzeAndUpdateTrends`();'
    conn.execute(query)
    conn.close()

def get_trends():
    conn = db.connect()
    query = 'SELECT L.LocationId, AVG(CAST(L.longitude AS DECIMAL(8, 4))) as avg_longitude, AVG(CAST(L.latitude AS DECIMAL(8, 4))) as avg_latitude, AVG(T.value) as avg_value FROM Locations L JOIN Trends T ON L.LocationId = T.LocationId GROUP BY L.LocationId;'
    query_result = conn.execute(query).fetchall()
    conn.close()
    return query_result