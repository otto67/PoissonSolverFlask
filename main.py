from flask import Flask, url_for, render_template, redirect, request, session, make_response
from markupsafe import escape
import json
import os
import Simulator as sim

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
    input_data = session['input']  
    input_data = json.loads(input_data)
    image_names = os.listdir('static')
    for i in image_names:
        if i.find('.png') < 0: # Remove CSS file from list
            image_names.remove(i)

    return render_template('results.html', result_data=image_names, input_data=input_data)
    

@app.route('/run_sim', methods=['POST'])
def run_sim():
    # Save for later use
    input_data = request.get_data()
    session['input'] = input_data.decode()
    
    # Convert to list before passing to simulator
    mylist = json.loads(input_data.decode())
    sim.run(mylist)
   
    image_names = os.listdir('static')   
    template_context = dict(added=image_names)
    return make_response(template_context)



if __name__ == "__main__":
    app.run(host ='0.0.0.0')  