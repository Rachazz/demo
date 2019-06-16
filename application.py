from flask import Flask,render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('assign3.html')

if __name__ == '__main__':
  app.run()

