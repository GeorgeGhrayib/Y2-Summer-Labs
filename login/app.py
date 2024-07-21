from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY']="*******"

firebaseConfig = {
  "apiKey": "AIzaSyAMc2fTVnV2eQNYvqaoZpuRIRRm2YAdmOY",
  "authDomain": "login-lab-e07aa.firebaseapp.com",
  "projectId": "login-lab-e07aa",
  "storageBucket": "login-lab-e07aa.appspot.com",
  "messagingSenderId": "198987525210",
  "appId": "1:198987525210:web:8afc11b01d7dd98f983c63",
  "measurementId": "G-LDKN1S3571",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html") 
    else: #if the method is post
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            login_session["quotes"] = []
            return redirect(url_for('home'))
        except:
            error = "Womp it failed sad"
            return render_template("login.html", error=error)

@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html") 
    else: #if the method is post
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            login_session["quotes"] = []
            return redirect(url_for('home'))
        except:
            error = "Womp it failed. Try again"
            return render_template("signup.html",error=error)
        
    
@app.route('/home', methods=["GET", "POST"])
def home():
    if login_session['user'] == None:
        return redirect(url_for('signup'))
    if request.method == "GET":
        return render_template("home.html")
    elif request.form['action'] == 'signout':
        login_session['user'] = None
        login_session["quotes"] = None
        auth.current_user = None
        return redirect(url_for('login'))
    else:
        login_session["quotes"].append(request.form['quote'])
        login_session.modified = True
        print(login_session["quotes"])
        return redirect(url_for('thanks'))

@app.route('/thanks', methods=["GET", "POST"])
def thanks():
    if login_session['user'] == None:
        return redirect(url_for('signup'))
    if request.method == "GET":
        return render_template("thanks.html")

@app.route('/display', methods=["GET", "POST"])
def display():
    if login_session['user'] == None:
        return redirect(url_for('signup'))
    if request.method == "GET":
        return render_template("display.html",qoutes=login_session["quotes"])


if __name__ == '__main__':
    app.run(debug=True)