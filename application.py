from flask import Flask,render_template
import mysql.connector
from mysql.connector import errorcode
import time

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
    start = time.time()
    cursor.execute("SELECT * FROM earthquake")
    row = cursor.fetchall()
    end = time.time()
    executiontime = end - start

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print('Done!!!')

    return render_template('searchearth.html',ci=row, t=executiontime)

@app.route('/multiplerun',methods=['POST','GET'])
def multiplrun():
    return render_template('count.html')#, t=exectime)

if __name__ == '__main__':
  app.run()

