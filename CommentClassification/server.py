from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from main import pre_process
import joblib
import numpy as np
import time

app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rating_prediction'
 
mysql = MySQL(app)
global emb
emb = joblib.load('tfidf.pkl')
global model
model = joblib.load('emb_model01.pkl')

@app.route('/get-all-comment', methods = ['GET'])
def getAllComment():
    if request.method == 'GET':
        try:
            cursor = mysql.connection.cursor()
            query = 'select * from rating' 
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            data_res = []
            for temp in data:
                data_res.append({
                    'comment' : temp[0],
                    'point' : temp[1]
                })
            print(data_res)
            cursor.close()
            return render_template('web.html', status = 200, data = data_res,msg = "ok") 
        except Exception:
            print(Exception)
            return render_template('web.html', status = 500, data = [],msg = "error") 

@app.route('/import', methods = ['POST'])
def predictMany():
    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()
            query = '' 
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            
            cursor.close()
            return 
        except Exception:
            print(Exception)

@app.route('/predict-one', methods = ['GET'])
def predictOne():
    if request.method == 'GET':
        try:
            comment = request.args.get("comment")
            print("=========")
            print(comment)
            comment = pre_process(comment)
            global emb
            input = emb.transform([comment])
            print(input)

            global model
            time1 = time.time()
            result = model.predict(input)[0]
            print("time to predict: ", time.time()-time1)
            print(result)

            cursor = mysql.connection.cursor()
            query = 'insert into rating(comment, point) values("'+comment+'",'+ str(result) +')' 
            print(query) 
            cursor.execute(query)
            mysql.connection.autocommit(True)
            cursor.close()
            return "0"
        except Exception as e:
            print(str(e))
            return "-"


app.run(host='localhost', port=5000)
    
