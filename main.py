from flask import Flask, url_for, render_template, redirect, request, session
from markupsafe import escape
import json
# from werkzeug.utils import redirect

# $env:FLASK_APP='main.py'
# $env:FLASK_ENV=development
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f43t56gyeutr'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():
 #    messages = request.args['messages']  # counterpart for url_for()
    messages = session['messages']       # counterpart for session
    print(json.loads(messages))
    messages = json.loads(messages)
        
    return render_template("results.html", myprms=[messages,'potato'])
    

@app.route('/run_sim', methods=['POST'])
def run_sim():
    names = request.get_data()  
    print("Running simulation")
    print("Input Parameters: \n" + names.decode())

    messages = json.dumps(names.decode())
    session['messages'] = messages
    return redirect(url_for('results'))
    # Or else do all processing here and create/return an html page containing the plots
    # return render_template('results.html')


if __name__ == "__main__":
    app.run(host ='0.0.0.0')  