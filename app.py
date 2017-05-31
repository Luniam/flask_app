from flask import Flask, render_template, request, json, session, redirect
import db

DEBUG = True
PORT = 5000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = 'your_desired_secret_key_here'

@app.route("/")
def index():
    flightDetails = db.getFlight()
    return render_template("index.html", flight = flightDetails)

#logging in
@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/validate',methods=['POST'])
def validate():
    try:
        clearSession()
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        data = db.validateUser(_email, _password)
        if len(data) > 0:
            session["user"] = data[0]
            session["name"] = data[1]
            session["lname"] = data[2]
            if data[3] > 0:
                session["admin"] = True
            return "success"
        else:
            return '<strong>Invalid email or password.</strong>'
    except Exception as e:
        return '<strong>An error occured, please try again.</strong>'

@app.route('/logout')
def logout():
    clearSession()
    return redirect('/')

def clearSession():
    session.pop('user', None)
    session.pop('name', None)
    session.pop('lname', None)
    session.pop('admin', None)
#logging in

#registering a user
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/signup", methods=["POST"])
def signup():
    first_name = request.form['inputName1']
    last_name = request.form['inputName2']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if first_name and last_name and _email and _password:
        if db.uniqueEmail(_email):
            if db.saveUser(first_name, last_name, _email, _password):
                return render_template("login.html", message = "Registered successfully.")
            else:
                return render_template("register.html", warning = "Something went wrong.")
        else:
            return render_template("register.html", warning = "Email address already exists.")
    else:
        return render_template("register.html", warning = "Enter all the required fields.")
#registering a user

@app.route("/user")
def user():
    if session.get("user"):
        userData = db.getUserData(session.get("user"))
        mapData = []
        for d in userData:
            fromC = db.getCodeName(d[0])
            toC = db.getCodeName(d[1])
            mapData.append(fromC)
            mapData.append(toC)
        return render_template("user.html", data = userData, md = mapData)
    else:
        return redirect('/login')

@app.route("/book")
def book():
    flightDetails = db.getFlight()
    if session.get("user"):
        return render_template("book.html", flight = flightDetails)
    else:
        return redirect("/login")

@app.route("/bookFlight", methods=["POST"])
def bookFlight():
    userid = session.get("user")
    if userid:
        flightid = request.form["flightId"];
        seatType = request.form["class"];
        amount = request.form["amount"];
        if int(amount) > 5:
            flightDetails = db.getFlight()
            return render_template("book.html", flight = flightDetails, warning = "Cannot book more than 5 tickets at once.")
        if int(amount) <= 0:
            flightDetails = db.getFlight()
            return render_template("book.html", flight = flightDetails, warning = "Number not allowed.")
        seat = 1
        if seatType == "Business":
            booking = [userid, flightid, amount, 0]
        else:
            booking = [userid, flightid, 0, amount]

        try:
            db.bookFlight(booking)
            return redirect("/book")
        except Exception as e:
            return "Sorry an error occured." + str(e)
    else:
        return redirect("/")

#admin area
@app.route("/admin")
def admin():
    if session.get("admin"):
        cityDetails = db.getCity()
        flightDetails = db.getFlight()
        return render_template("admin.html", city = cityDetails, flight = flightDetails)
    else:
        return redirect('/')

@app.route("/makeFlight", methods=["POST"])
def makeFlight():
    if session.get("admin"):
        fromCity = db.getName(request.form["fromCity"])
        toCity = db.getName(request.form["toCity"])
        month = request.form["month"]
        day = request.form["day"]
        businessTicket = request.form["businessTicket"]
        businessPrice = request.form["businessPrice"]
        economyTicket = request.form["economyTicket"]
        economyPrice = request.form["economyPrice"]
        flight = [fromCity, toCity, month, day, businessTicket, businessPrice, economyTicket, economyPrice]
        try:
            if db.saveFlight(flight):
                return redirect("/admin")
            else:
                return "Sorry an error occured. Please try again."
        except Exception as e:
            return "Sorry an error occured. Probably the same flight already exists."
    else:
        return redirect("/")

@app.route("/deleteFlight", methods=["POST"])
def deleteFlight():
    if session.get("admin"):
        flightId = request.form["flightId"]
        try:
            if db.deleteFlight(flightId):
                return redirect("/admin")
            else:
                return "Sorry an error occured. Please try again."
        except Exception as e:
            return "Sorry an error occured. Probably the flight does not exist."
    else:
        return redirect("/")

@app.route("/check")
def check():
    return str(db.getUserData(session.get("user")))

#test code

def main():
    db.initializeDB(app)
    app.run(debug = DEBUG, host = HOST, port = PORT)

if __name__ == '__main__':
    main()