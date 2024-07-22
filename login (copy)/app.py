from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY']="*******"

firebaseConfig = {
  'apiKey': "AIzaSyBJhI8eARfBJZF_RAm-W7ygq5XVjb5aV9k",
  'authDomain': "date-base-lab.firebaseapp.com",
  'projectId': "date-base-lab",
  'storageBucket': "date-base-lab.appspot.com",
  'messagingSenderId': "120564488470",
  'appId': "1:120564488470:web:b91d3fb5fb06a7ce675837",
  'measurementId': "G-YYWXL1GC1K",
  "databaseURL": "https://date-base-lab-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html") 
    else: #if the method is post
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
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
        fullname = request.form["fullname"]
        username = request.form['username']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            db.child("users").child(user_id).set({
                "fullname": fullname,
                "username": username,
                "email": email
            })
            login_session['user'] = user
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
        auth.current_user = None
        return redirect(url_for('login'))
    else:
        qoute = {"text":request.form['quote'],"said_by":request.form['speaker'],"uid":login_session['user']['localId']}
        db.child("Qoutes").push(qoute)
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
        Qoutes=db.child("Qoutes").get().val()
        return render_template("display.html",qoutes=Qoutes)


if __name__ == '__main__':
    app.run(debug=True)