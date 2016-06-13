from flask import Flask

application = Flask(__name__)


@application.route('/')
def index():
    return 'This is the beginning of the test applicaton'


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=9000)
