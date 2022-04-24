import pandas as pd
import sqlalchemy

conn = sqlalchemy.create_engine('mysql+pymysql://root@localhost/test')

data = pd.read_excel('default.xlsx')
data['dob'] = pd.to_datetime(data['dob']).dt.date
js = data.to_json(orient='records', date_format="iso", date_unit='s')
data1 = pd.read_json('[{"name":"santu","age":24,"dob":897696000000},{"name":"sampan","age":25,"dob":847929600000},{"name":"izaz","age":23,"dob":906508800000}]')
