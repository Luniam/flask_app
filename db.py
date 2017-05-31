import time
from flask import json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()

def initializeDB(app):
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'your_password_here'
    app.config['MYSQL_DATABASE_DB'] = 'db_name'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

def uniqueEmail(email):
    queryString = "SELECT COUNT(*) FROM user WHERE email = %s"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (email))
    data = cursor.fetchall()
    connection.close()
    if data[0][0] > 0:
        return False
    else:
        return True

def saveUser(firstName, lastName, email, _password):
    password = generate_password_hash(_password)
    queryString = "INSERT INTO user (firstName, lastName, email, password) VALUES (%s,%s,%s,%s)"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (firstName, lastName, email, password))
    data = cursor.fetchall()
 
    if len(data) == 0:
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

def saveAdmin(firstName, lastName, email, _password):
    password = generate_password_hash(_password)
    queryString = "INSERT INTO user (firstName, lastName, email, password, isAdmin) VALUES (%s,%s,%s,%s,%s)"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (firstName, lastName, email, password, "1"))
    data = cursor.fetchall()
 
    if len(data) == 0:
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

def validateUser(email, password):
    queryString = "SELECT id, firstName, lastName, isAdmin, password FROM user WHERE email = %s"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (email,))
    data = cursor.fetchall()
    connection.close()

    if len(data) > 0:
        if check_password_hash(data[0][4], password):
            return data[0][0:4] #return the user id, firstName, lastName, isAdmin in a tuple
    return () #return an empty tuple if password does not match

def getCity():
    queryString = "SELECT * FROM airport"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString)
    data = cursor.fetchall()
    connection.close()

    if len(data) > 0:
        return data
    else:
        return 0

def saveFlight(flight):
    queryString = "INSERT INTO flight (fromCity, toCity, month, day, business, businessPrice, economy, economyPrice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (flight[0], flight[1], flight[2], flight[3], flight[4], flight[5], flight[6], flight[7]))
    data = cursor.fetchall()
 
    if len(data) == 0:
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

def getName(codeName):
    queryString = "SELECT name FROM airport WHERE codeName = %s"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (codeName))
    data = cursor.fetchall()
    connection.close()

    if len(data) > 0:
        return data
    else:
        return ()

def getCodeName(name):
    queryString = "SELECT codeName FROM airport WHERE name = %s"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (name))
    data = cursor.fetchall()
    connection.close()

    if len(data) > 0:
        return data
    else:
        return ()

def getFlight():
    queryString = "SELECT * FROM flight ORDER BY fromCity, toCity"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString)
    data = cursor.fetchall()
    connection.close()

    if len(data) > 0:
        return data
    else:
        return ()

def deleteFlight(flightId):
    queryString = "DELETE FROM flight WHERE id = %s"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (flightId))
    data = cursor.fetchall()
 
    if len(data) == 0:
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


def bookFlight(booking):
    queryString = "INSERT INTO booking (userId, flightId, business, economy) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE business = business+" + str(booking[2]) +  ",economy = economy + " + str(booking[3])

    if booking[3] == 0:
        queryString2 = "UPDATE flight AS f1 INNER JOIN flight AS f2 ON f1.id = f2.id SET f1.business = f2.business - " +  booking[2] + " WHERE f1.id = %s;"
    elif booking[2] == 0: 
        queryString2 = "UPDATE flight AS f1 INNER JOIN flight AS f2 ON f1.id = f2.id SET f1.economy = f2.economy - " +  booking[3] + " WHERE f1.id = %s;"

    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (booking[0], booking[1], booking[2], booking[3]))
    connection.commit()
    connection.close()
    
    connection2 = mysql.connect()
    cursor2 = connection2.cursor()
    cursor2.execute(queryString2, (booking[1]))
    connection2.commit()
    connection2.close()

def getUserData(userId):
    queryString = "SELECT flight.fromCity, flight.toCity, flight.month, flight.day, T.business, T.economy, flight.id, T.flightId  FROM (SELECT booking.flightId, booking.business, booking.economy FROM booking WHERE userId = %s) AS T INNER JOIN flight ON T.flightId = flight.id"

    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(queryString, (userId))
    data = cursor.fetchall()
    connection.close()

    if len(data) > 0:
        return data
    else:
        return ()