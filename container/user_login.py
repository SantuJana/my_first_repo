from flask import request,jsonify
import pandas as pd
import json
from dbConnection import mysql_conn as conn

def logIn():
    if request.method == 'POST':
        if 'email' and 'password' not in request.form:
            return jsonify({'login_status':'failed','message':'body part missing.','data':''})
        email = request.form['email']
        password = request.form['password']
        if email=='' or password == '':
            return jsonify({'login_status':'failed','message':'email or password missing.','data':''})

        if email !='' and password !='':
            data = pd.read_sql(f"select id, name, email, phone from user where email='{email}' and password='{password}'", con=conn)
            if len(data)>0:
                result = {
                    'login_status':'success',
                    'message':'successfully loged in.',
                    'data': json.loads(data.to_json(orient='records'))
                }
                return jsonify(result)
            else:
                return jsonify({'login_status':'failed','message':'email or password does not match','data':''})

