import graph

from flask import Flask
from flask import render_template

import os

app = Flask(__name__)

@app.route('/')
def front_page():
	people = graph.people()
	return render_template('index.html', people = people)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port = port, debug = True)