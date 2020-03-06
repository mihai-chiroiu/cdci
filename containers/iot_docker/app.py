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


@app.route('/init')
def init():
    """
        Delete all information
    """
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    connection = db.cursor()
    try:
        connection.execute("delete from sensors")
        db.commit()
    except:
        db.rollback()
    db.close()
    return redirect("/")
    
@app.route("/update/", methods=["GET","PUT"] )
@app.route("/update/<sensorid>", methods=["GET","PUT"] )
def update(sensorid=None):
    sensorTempStr = request.args.get('temperature') 
    if sensorTempStr == None or sensorid == None:
        return "usage: update/sensorid?temperature=VALUE"
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    cursor = db.cursor()
    try:
        query="update sensors set temperature = '" + sensorTempStr + "' where id = '" + sensorid + "';"
        print(query)
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        return "FAIL"
    db.close()
    return "OK"

@app.route("/add/", methods=["GET","PUT"] )
@app.route("/add/<sensor_name>", methods=["GET","PUT"] )
def add(sensor_name=None):
    sensorTempStr = request.args.get('temperature') 
    if sensorTempStr == None or sensor_name == None:
        return "usage: update/sensor_name?temperature=VALUE"
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    cursor = db.cursor()
    try:
        #query="insert into sensors(name,temperature) values ('" + sensor_name + "','" + sensorTempStr + "');"
        query="insert into sensors(name,temperature) values ('" + db.escape_string(sensor_name).decode("UTF-8") + "','" + db.escape_string(sensorTempStr).decode("UTF-8") + "');"
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        return "FAIL"
    db.close()
    return "OK"




@app.route("/", methods=["GET", "PUT"])
def default():
    """
        Show list of comments with form to submit comments
    """
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    cursor = db.cursor()
    cursor.execute('''select * from sensors''')
    comments = cursor.fetchall()
    db.close()
    completeTable="<tr >"
    completeTable += "<th> No. </th>"
    completeTable += "<th> Name </th>"
    completeTable += "<th> Temperature </th>"
    completeTable += "<th> Status </th>"
    completeTable+="</tr>"
    for c in comments:
        completeTable+="<tr >"
        completeTable += "<th>" + str(c[0]) + "</th>"
        completeTable += "<th>" + str(c[1]) + "</th>"
        completeTable += "<th>" + str(c[2]) + "</th>"
        if bool(random.getrandbits(1)):
            completeTable += "<th> ON </th>"
        else:
            completeTable += "<th> OFF </th>"
        completeTable+="</tr>"
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Sensors data</h1>
        <table border=\"1\">
        %s
        </table>
    </body>
    </html>
    """ %(completeTable)

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=True, use_evalex=False)
