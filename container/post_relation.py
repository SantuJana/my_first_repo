import pandas as pd
import numpy as np
import sys
import json
from dbConnection import mysql_conn as conn
from flask import request
    
def getRelation():  
    if request.method=="POST":
        tbl1 = request.form['table1']
        tbl2 = request.form['table2'] 
    tbl1_col=[]
    tbl2_col=[]
    match=[]
    relation=[]
    def getRelation(col1, col2):
        non1 = df1[col1].dropna()
        non2 = df2[col2].dropna()
        unq1 = non1.unique()
        unq2 = non2.unique()
        data_count = max(len(unq1),len(unq2))
        mrg = pd.Series(np.intersect1d(unq1, unq2))
        common_data = len(mrg)

        if data_count!=0:
            percentage = int((100/data_count)*common_data)
            if percentage != 0:
                # print(f'{table1}-> '+col1+' & '+f'{table2}-> '+col2)
                # print(str(percentage)+' %')
                p=str(percentage)+' %'
                tbl1_col.append(col1)
                tbl2_col.append(col2)
                match.append(p)
      
                data1_len = len(pd.merge(pd.Series(non1, name='key'),pd.Series(mrg, name='key'), how='inner'))
                data2_len = len(pd.merge(pd.Series(non2, name='key'),pd.Series(mrg, name='key'), how='inner'))
                if data1_len==common_data:
                    if data2_len==common_data:
                        # print('One to One\n')
                        relation.append('One to One')
                    else:
                        # print('One to Many\n')
                        relation.append('One to Many')
                else:
                    if data2_len==common_data:
                        # print('Many to One\n')
                        relation.append('Many to One')
                    else:
                        # print('Many to Many\n')
                        relation.append('Many to Many')
    

    table1 = tbl1.strip()
    table2 = tbl2.strip()

    
    data1 = pd.read_sql(f"SELECT column_name, data_type FROM information_schema.columns WHERE TABLE_NAME='{table1}'", con=conn)
    data2 = pd.read_sql(f"SELECT column_name, data_type FROM information_schema.columns WHERE TABLE_NAME='{table2}'", con=conn)

    if (data1.empty or data2.empty):
    #     print('Table name invalide.')
            sys.exit('Table name invalid.')

    tbl1_var = data1.loc[data1["DATA_TYPE"]=='varchar',["COLUMN_NAME"]]["COLUMN_NAME"]
    tbl2_var = data2.loc[data2["DATA_TYPE"]=='varchar',["COLUMN_NAME"]]["COLUMN_NAME"]

    varchar1 = ", ".join(tbl1_var)
    varchar2 = ", ".join(tbl2_var)

    tbl_int1 = data1.loc[data1["DATA_TYPE"]=='int',["COLUMN_NAME"]]["COLUMN_NAME"]
    tbl_int2 = data2.loc[data2["DATA_TYPE"]=='int',["COLUMN_NAME"]]["COLUMN_NAME"]

    int1 = ", ".join(tbl_int1)
    int2 = ", ".join(tbl_int2)

    tbl_date1 = data1.loc[data1["DATA_TYPE"]=='date',["COLUMN_NAME"]]["COLUMN_NAME"]
    tbl_date2 = data2.loc[data2["DATA_TYPE"]=='date',["COLUMN_NAME"]]["COLUMN_NAME"]

    date1 = ", ".join(tbl_date1)
    date2 = ", ".join(tbl_date2)

                # print(f'varchar:\n {table1} - '+varchar1+f'\n {table2} - '+varchar2+'\n')
                # print(f'numeric:\n {table1} - '+int1+f'\n {table2} - '+int2+'\n')
                # print(f'date:\n {table1} - '+date1+f'\n {table2} - '+date2+'\n')

    df1 = pd.read_sql(f'{table1}', con=conn)
    df2 = pd.read_sql(f'{table2}', con=conn)
    
    # print('--------------Data Relation------------')

    if not tbl1_var.empty and not tbl2_var.empty:
        for col1 in tbl1_var:
            for col2 in tbl2_var:
                getRelation(col1, col2)

    if not tbl_int1.empty and not tbl_int2.empty:
        for col1 in tbl_int1:
            for col2 in tbl_int2:
                getRelation(col1, col2)

    if not tbl_date1.empty and not tbl_date2.empty:
        for col1 in tbl_date1:
            for col2 in tbl_date2:
                getRelation(col1, col2)

    # print('-------------Completed---------------')
    df = pd.DataFrame({"tbl1_col":tbl1_col,"tbl2_col":tbl2_col,"match":match,"relation":relation})
    dt = df.to_json(orient='records')
    result = {
        "left_table":tbl1,
        "right_table":tbl2,
        "varchar_left":varchar1,
        "varchar_right":varchar2,
        "numeric_left":int1,
        "numeric_right":int2,
        "date_left":date1,
        "date_right":date2,
        "relation":json.loads(dt),
    }

    return(result)
