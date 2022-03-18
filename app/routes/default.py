from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/test')
# def test():
#     return render_template('test.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

@app.route('/research')
def research():
    return render_template('research.html')