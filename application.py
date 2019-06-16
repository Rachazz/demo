from flask import Flask
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! Assignmnet3 getting hang of it-perfect"

if __name__ == '__main__':
  app.run()

