from wsgi.main import application, init_db

init_db()

application.run(host='0.0.0.0', debug=True, port=9000)
