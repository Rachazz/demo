from flask import Flask,render_template,request
import mysql.connector

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


if __name__ == '__main__':
  app.run()

