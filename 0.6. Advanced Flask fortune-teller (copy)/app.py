from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:     
        month = request.form['month']
        return redirect(url_for('fortune',m=month))

@app.route('/fortune/<m>')
def fortune(m):
    if(len(m)>10):
        return render_template("fortune.html", month = fortunes[9])
    return render_template("fortune.html", month = fortunes[len(m)-1])

if __name__ == '__main__':
    app.run(debug = True)