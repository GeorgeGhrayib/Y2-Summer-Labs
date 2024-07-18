from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session

app = Flask(__name__)
app.config['SECRET_KEY']="PASSWORD"

fortunes=["you will die",
"you will die again",
"fine you will live",
"your live is meaningless",
"ew",
"get a life",
"WOOO",
"you get dog.",
"you get cat.",
"nothing"
]

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    else:     
        login_session["name"] = request.form['name']
        login_session["month"] = request.form['month']
        return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html', name=login_session["name"], month = login_session['month'])
    else:     
        return redirect(url_for('fortune',m = login_session['month'],f=True))

@app.route('/home/<f>')
def fortune(f):
    if(len(login_session['month'])>10):
        return render_template("home.html", ff = fortunes[len(login_session['month'])], flag = True, name=login_session["name"], month = login_session['month'])
    return render_template("home.html", ff = fortunes[len(login_session['month'])], flag = True, name=login_session["name"], month = login_session['month'])


if __name__ == '__main__':
    app.run(debug = True)