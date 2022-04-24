import sqlalchemy
import pandas as pd

USER_NAME= 'root'
PASSWORD = ''
DATABASE= 'test'
HOST= '@localhost'
PORT= '3306'

mysql_conn = sqlalchemy.create_engine(f'mysql+pymysql://{USER_NAME}{HOST}/{DATABASE}')

