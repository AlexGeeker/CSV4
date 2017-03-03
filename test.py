from flask import Flask,render_template
import os
app = Flask(__name__)

@app.route('/')

def index():

    return app.root_path+os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    app.run(debug=True)