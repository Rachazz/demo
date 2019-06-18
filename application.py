from flask import Flask,render_template,request
import mysql.connector

import time
import redis
import hashlib
import pickle


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
    print("Connection")
    row=[]
    if request.method=="POST":
        num=int(request.form['num'])
        magni1=request.form['m1']
        magni2=request.form['m2']
        start = time.time()
        for i in range(1,num):
            #query="SELECT * FROM earthquake"
            #query='select count(*) from earthquake where "mag">\''+magni+'\''
            #query='select count(*) from earthquake where "mag" between \''+magni1+'\' and \''+magni2+'\''
            query='select "depth" from earthquake where "mag"=2'
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
        magni1=request.form['m1']
        magni2=request.form['m2']

        start = time.time()
        for i in range(0,int(num)):
            #query=cursor.execute("SELECT * FROM earthquake")
            #query="SELECT * FROM earthquake"
            #query='select count(*) from earthquake where "mag">\''+magni+'\''
            #query='select count(*) from earthquake where "mag" between \''+magni1+'\' and \''+magni2+'\''
            query='select "depth" from earthquake where "mag"=2'
            hash = hashlib.sha224(query.encode('utf-8')).hexdigest()
            key="redis_cache:"+hash
            if (r.get(key)):
                print("redis cached!")
            else:
                cursor.execute(query)
                row = cursor.fetchall()
                rows = []
                for j in row:
                    rows.append(str(j))
                # Put data into cache for 1 hour
                r.set(key, pickle.dumps(list(rows)) )
                r.expire(key, 36);
        end=time.time()
        executiontime = end - start
        return render_template('count.html', t=executiontime)



if __name__ == '__main__':
  app.run()

