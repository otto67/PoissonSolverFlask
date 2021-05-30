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

@app.route('/results', methods=['PUT'])
def results():
 #    messages = request.args['messages']  # counterpart for url_for()
    messages = session['messages']       # counterpart for session
    print(json.loads(messages))
    messages = json.loads(messages)
    # return app.send_static_file('templates\results.html')
    # if request.method == 'GET':
    
    content = render_template("results.html", myprms=[json.dumps(messages),"potato"])
    return Response(
            content,
            content_type='text/javascript; charset=UTF-8'
        )

#   return render_template('results.html', my_data=messages, p1='potato')


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