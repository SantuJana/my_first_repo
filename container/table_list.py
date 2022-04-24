from flask import jsonify
from dbConnection import mysql_conn, DATABASE
import pandas as pd

def table_list():
    try:
        sql = f"SELECT substr(TABLE_NAME,4,length(TABLE_NAME)) as 'table_name' from information_SCHEMA.TABLES WHERE TABLE_SCHEMA='{DATABASE}' AND LEFT(TABLE_NAME,3)='at_'"
        data = pd.read_sql(sql, con=mysql_conn)
        result = {'status':'success', 'data': list(data["table_name"])}
        return jsonify(result)
    except Exception as e:
        return jsonify({'status':'failed','message':str(e.__cause__)})