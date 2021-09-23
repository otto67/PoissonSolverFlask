import re
from typing import get_args
from flask import Flask, url_for, render_template, redirect, request, session, make_response, jsonify
from markupsafe import escape
import json 
import os

from numpy import imag
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
    # Save for use in listing input in results page
    input_data = request.get_data()
    session['input'] = input_data.decode()
    
    # Convert to list before passing to simulator
    mylist = json.loads(input_data.decode())
    sim.run(mylist)
   
    image_names = os.listdir('static')
    retval = []
    for i in image_names:
        if i.find('.png') : # Remove CSS file from list
            retval.append('/results')    
    
    template_context = jsonify(retval)
    return make_response(template_context)

@app.route('/test', methods=['GET'])
def test():
    print("Serving test request")
    image_names = os.listdir('static')

    print(request.headers)

    return jsonify(image_names)

@app.route('/test2', methods=['GET', 'POST'])
def test2():

    print("Serving test 2 request is " + request.method)    

    if request.method == 'GET':
        retval = {}
        retval['first'] = 'myfirst'
        retval['second'] = 'mysecond'
    else:
        print("POST request, got " + json.loads(request.data.decode()))
        retval = request.data.decode()


    print(request.headers)

    return jsonify(retval)


if __name__ == "__main__":
    app.run(host ='0.0.0.0')  