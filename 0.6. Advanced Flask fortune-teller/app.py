from flask import Flask, render_template
import random
 
app = Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

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

@app.route('/fortune')
def furtune():
    index = random.randint(0, 9)
    return render_template("fortune.html",Fortune = fortunes[index])

@app.route('/indecisive')
def indecisive():
    index = random.randint(0, 9)
    extra1 = random.randint(0, 9)
    while extra1 == index:
        extra1 = random.randint(0, 9)
    extra2 = random.randint(0, 9)
    while extra1 == extra2 or extra2 == index:
        extra2 = random.randint(0, 9)
    Fortunes = [fortunes[index],fortunes[extra1],fortunes[extra2]]
    return render_template("indecisive.html",Fortunes = Fortunes)

if __name__ == '__main__':
    app.run(debug = True)