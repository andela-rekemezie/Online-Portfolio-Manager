#!/usr/bin/python
import os

# virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtenv, dict(__file__=virtenv))
except IOError:
    pass

from main import application

# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     httpd = make_server('localhost', 8051, application)
#     # Wait for a single request, serve it and quit.
#     httpd.serve_forever()
