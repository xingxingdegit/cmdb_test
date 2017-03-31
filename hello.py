#!/usr/bin/env python
#
from flask import Flask,url_for
app = Flask(__name__)
#app.debug = True
#app.config['DEBUG'] = True
app.debug = True

@app.route('/file/<username>')
def hello_world(username):
    return 'Hello %s\n' % username

@app.route('/route/<filename>')
def test_route(filename):
    return filename

@app.route('/static/<filename>')
def Static(filename):
    filename = 'static/' + filename
    try:
        fd = open(filename)
        
        return 'open succesful' + fd.read()
    except Exception:
        return 'test error\n'

with app.test_request_context():
    print url_for('hello_world',username='ss tt')
  #  print url_for('test_route',filename='ss')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
