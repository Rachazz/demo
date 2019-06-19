from flask import Flask,render_template,request
import mysql.connector

import time
import redis
import hashlib
import pickle
import random


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

@app.route('/withoutcache',methods=['POST','GET'])
def displaydata():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Connection...")
    row=[]
    if request.method=="POST":
        num=int(request.form['num'])
        d1=float(request.form['d1'])
        d2=float(request.form['d2'])

        start = time.time()
        for i in range(0,num):
            mag1= round(random.uniform(d1, d2),1)
            mag2= round(random.uniform(d1, d2),1)


            query='select * from earthquake where "depthError" between '+str(mag1)+' and '+str(mag2)+''
            cursor.execute(query)
            row = cursor.fetchall()
        end = time.time()
        executiontime = end - start
        return render_template('searchearth.html',ci=row, t=executiontime)
    #return render_template('assign3.html')

@app.route('/rediscache',methods=['POST','GET'])
def multiplrun():

    myHostname = "assign3.redis.cache.windows.net"
    myPassword = "k3KsDLYj7yQIocfH7Wz3VwLOoI2z2iPSdomO1nixvKo="
    conn = mysql.connector.connect(**config)
    r = redis.StrictRedis(host=myHostname, port=6380,db=0,password=myPassword,ssl=True)
    cursor = conn.cursor()


    if request.method=="POST":
        num=int(request.form['num'])
        d1=float(request.form['d1'])
        d2=float(request.form['d2'])

        start = time.time()
        for i in range(0,int(num)):
            mag1= round(random.uniform(d1, d2),1)
            mag2= round(random.uniform(d1, d2),1)

            query='select * from earthquake where "depthError" between '+str(mag1)+' and '+str(mag2)+''
            hash = hashlib.sha224(query.encode('utf-8')).hexdigest()
            key="redis_cache:"+hash
            ### 1st method
            if (r.get(key)):
                print("redis cached!")
            else:
                cursor.execute(query)
                row = cursor.fetchall()
                rows = []
                for j in row:
                    rows.append(str(j))
                # Put data into cache for 1 hour
                r.set(key, pickle.dumps(list(rows)))
            ### 2nd method
            '''
            result = r.get(key)

            if not result:
                cursor.execute(query)
                row = cursor.fetchall()
                r.set(key, row)
            '''
        end=time.time()
        executiontime = end - start
        return render_template('count.html', t=executiontime)


@app.route('/display',methods=['POST','GET'])
def display():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Connection...")
    row=[]
    if request.method=="POST":

        d1=request.form['d1']
        print(d1)
        d2=request.form['d2']
        print(d2)
        print("values depth")
        long1=request.form['long1']
        print(long1)
        query='select count(*) from earthquake where "depthError">1'
        #query='select * from earthquake where "depthError" between \''+d1+'\' and \''+d2+'\' and "longitude"> \''+long1+'\''
        print("query")
        cursor.execute(query)
        row = cursor.fetchall()
        print(row)
        print("fetching")
        return render_template('display_values.html',value=row)
    #return render_template('assign3.html')

if __name__ == '__main__':
  app.run()

