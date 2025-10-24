import os
from flask import Flask, request, redirect
import datetime
import random
import MySQLdb


app = Flask(__name__)
db_user = "vulnUser"
db_password = "vulnPassword"
db_address = "localhost"
db_database = "vulnSensors"

@app.route("/", methods=["GET", "PUT"])
def default():
    """
        Show list of comments with form to submit comments
    """
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Sensors data</h1>
        <table border=\"1\">
        </table>
    </body>
    </html>
    """

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=True, use_evalex=False)
