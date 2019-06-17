from flask import Flask,render_template,request
import mysql.connector

import time
import redis



app = Flask(__name__)

config = {
  'host':'demoquakes.mysql.database.azure.com',
  'user':'quakes@demoquakes',
  'password':'Earth_quake',
  'database':'equakes'
}


@app.route("/")
def index():
    return render_template('assign3.html')

@app.route('/displaydata',methods=['POST','GET'])
def displaydata():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Connection")
    row=[]
    if request.method=="POST":
        num=int(request.form['num'])
        start = time.time()
        for i in range(1,num):
            cursor.execute("SELECT * FROM earthquake")
            row = cursor.fetchall()
        end = time.time()
        executiontime = end - start
        return render_template('searchearth.html',ci=row, t=executiontime)
    #return render_template('assign3.html')


if __name__ == '__main__':
  app.run()

