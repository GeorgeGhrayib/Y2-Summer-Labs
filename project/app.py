from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY']="*******"

firebaseConfig = {
  'apiKey': "AIzaSyChIf7h3QL_g6uo7DqipCsI8VzMidTISPs",
  'authDomain': "personal-project-meet-y2.firebaseapp.com",
  'projectId': "personal-project-meet-y2",
  'storageBucket': "personal-project-meet-y2.appspot.com",
  'messagingSenderId': "575272609579",
  'appId': "1:575272609579:web:ea6cd1c63f483c0fb8476e",
  'measurementId': "G-WY42HCE41R",
  'databaseURL':"https://personal-project-meet-y2-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html") 
    elif request.form['action'] == 'signin':
        return redirect(url_for('signin'))
    else: 
        return redirect(url_for('signup'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html") 
    else:
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
                "email": email,
                "level": 1
            })
            login_session['user'] = user
            return redirect(url_for('dashboard'))
        except:
            error = "Womp it failed. Try again!"
            return render_template("signup.html",error=error)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html") 
    else:
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('dashboard'))
        except:
            error = "Womp it failed. Try again!"
            return render_template("signin.html", error=error)
        
    
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if login_session['user'] == None:
        return redirect(url_for('index'))
    if request.method == 'GET':
        user = db.child("users").child(login_session['user']['localId']).get().val()
        sdic = {}
        if 'songs' in user:
            for song in user['songs']:
                storage.child(user['songs'][song]).download(user['songs'][song],"static/"+user['songs'][song])
                sdic[song]=user['songs'][song]
        return render_template("dashboard.html",level = user['level'],name = user['fullname'], sdic = sdic) 
    elif request.form['action'] == 'signout':
        login_session['user'] = None
        auth.current_user = None
        return redirect(url_for('index'))
    elif request.form['action'] == 'profile':
        return redirect(url_for('profile'))
    elif request.form['action'] == 'songlist':
        return redirect(url_for('songlist'))
    else: 
        try:
            path_on_cloud = str(db.child("index").get().val())
            c = db.child("index").get().val()
            db.child("index").set(c+1)
            path_local = request.form["file"]
            if path_local[path_local.find('.'):] != ".ogg":
                return redirect(url_for('dashboard'))
            c = db.child("users").child(login_session['user']['localId']).child("level").get().val()
            db.child("users").child(login_session['user']['localId']).child("level").set(c+1)
            path_on_cloud+=path_local[path_local.find('.'):]
            storage.child(path_on_cloud).put(path_local)
            db.child("users").child(login_session['user']['localId']).child("songs").child(request.form['name']).set(path_on_cloud)
            return redirect(url_for('dashboard'))
        except:
            return redirect(url_for('dashboard'))
        

@app.route('/profile', methods=["GET", "POST"])
def profile():
    if login_session['user'] == None:
        return redirect(url_for('index'))
    if request.method == 'GET':
        user = db.child("users").child(login_session['user']['localId']).get().val()
        return render_template("profile.html",name = user["fullname"],username=user["username"],email=user["email"],level=user["level"])
    elif request.form['action'] == 'save':
        fullname = request.form["name"]
        username = request.form['username']
        if fullname != '':
            user = db.child("users").child(login_session['user']['localId']).get().val()
            user['fullname'] = fullname
            db.child("users").child(login_session['user']['localId']).set(user)
        if username != '':
            user = db.child("users").child(login_session['user']['localId']).get().val()
            user['username'] = username
            db.child("users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('profile'))
    elif request.form['action'] == 'dashboard':
        return redirect(url_for('dashboard')) 

@app.route('/songlist', methods=["GET", "POST"])
def songlist():
    if login_session['user'] == None:
        return redirect(url_for('index'))
    if request.method == 'GET':
        users = db.child("users").get().val()
        for user_id in users:
            user = users[user_id]
            if 'songs' in user:
                for song in user['songs']:
                    storage.child(user['songs'][song]).download(user['songs'][song],"static/"+user['songs'][song])
        return render_template("songlist.html",users=users)
    elif request.form['action'] == 'dashboard':
        return redirect(url_for('dashboard')) 
    elif request.form['action'] == 'signout':
        login_session['user'] = None
        auth.current_user = None
        return redirect(url_for('index')) 


if __name__ == '__main__':
    app.run(debug=True)