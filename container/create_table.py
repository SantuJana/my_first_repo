
from lzma import FORMAT_ALONE
from operator import index
from flask import request,jsonify
from numpy import dtype, int64, integer
import pandas as pd
from dbConnection import mysql_conn as conn 
import json
from sqlalchemy.types import VARCHAR, Integer

def create_table():
    if request.method == 'POST':
        data = request.json['data']
        table_name = request.json['table_name']
        table_name = 'at_'+table_name
        
        df = pd.read_json(json.dumps(data))
        df1 = pd.DataFrame(df)
        # df1['dob']=pd.to_date(df['dob'])
        # df1['id']=df1['id'].astype(int64)
        df1.to_sql(table_name,con=conn, if_exists='append', index=False)
        return 'ok'