from flask import Flask , render_template , request
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

app.debug = True
app.secret_key = "your_secret_key"



@app.route("/")
def hello_world():
    return render_template('index.html')

from controller import *

# @app.errorhandler(OperationalError)
# def handle_operational_error(error):
#     app.logger.error(f"OperationalError: {str(error)}")
#     return render_template('error.html', message="An error occurred while processing your request."), 500


if __name__ == '__main__':
    app.run(debug=True) 