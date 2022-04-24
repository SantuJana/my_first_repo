from flask import Flask, jsonify
from flask_cors import CORS
from container import post_relation, upload_file, user_login, create_table, table_list
import pandas as pd
from dbConnection import mysql_conn as conn


app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER']="H:\\Flask API\\static\\uploaded"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=['POST'])
def login():
    return user_login.logIn()

@app.route("/employee")
def getEmployee():
    data = pd.read_sql('employee',con=conn)
    jsn_data = data.to_json(orient='records')
    return(jsn_data)


    
@app.route("/relation", methods=["POST"])
def getrelation():
    result = post_relation.getRelation()
    return(jsonify(result))

@app.route("/upload_file", methods=["POST"])
def uploadFile():
    return upload_file.upload_file(app.config['UPLOAD_FOLDER'])

@app.route("/api/table_list")
def tableList():
    return table_list.table_list()

@app.route("/api/create_table", methods=['POST'])
def createTable():
    return create_table.create_table()

if __name__=="__main__":
    app.run(debug=True)
