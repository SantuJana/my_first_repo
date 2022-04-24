import json
from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
import pandas as pd

ALLOWED_EXTENSIONS = {'csv','xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def upload_file(upload_location):
    if request.method == "POST":
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']

        if file.filename =='':
            return 'No selected file'

        if file and allowed_file(file.filename):
            f_name = secure_filename(file.filename)
            f_path = os.path.join(upload_location,f_name)
            try:
                file.save(f_path)
                f_path = f_path.replace('\\','/')

                if file_extension(f_name)=='csv':
                    try:
                        df = pd.read_csv(f_path)
                        data = df.to_json(orient='records')
                        table_name = f_name.rsplit('.',1)[0]
                        data_types = list(df.dtypes.astype(str).replace(['int64','object','float64','datetime64[ns]'],['int','varchar','float','datetime']))
                        response = {
                            'upload_status': 'success',
                            'table_name': table_name,
                            'columns': list(df.columns),
                            'data_types': data_types,
                            'data': json.loads(data),
                        }
                        return jsonify(response)
                    except:
                        return jsonify({'upload_status': 'failed','message':'unable to read file'})

                if file_extension(f_name)=='xlsx':
                    xlreader = pd.ExcelFile(f_path)
                    sheets = xlreader.sheet_names

                    f_result = []
                    for sheet in sheets:
                        data = xlreader.parse(sheet_name=sheet)
                        j_data = data.to_json(orient='records')
                        data_types = list(data.dtypes.astype(str).replace(['int64','float64','object','datetime64[ns]'],['int','float','varchar','datetime']))
                        result = {
                            'table_name':sheet,
                            'data': json.loads(j_data),
                            'columns': list(data.columns),
                            'data_types': data_types,
                        }
                        f_result.append(result)

                    return jsonify({'upload_status':'success','data':f_result})

            except Exception as e:
                return jsonify({'upload_status': 'failed','message':str(e.__cause__)})

        else:
            return jsonify({'upload_status': 'failed','message':'File format not allowed.'})