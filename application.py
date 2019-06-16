from flask import Flask,render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

config = {
  'host':'demoquakes.mysql.database.azure.com',
  'user':'quakes@demoquakes',
  'password':'Earth_quake',
  'database':'quakes'
}


@app.route("/")
def index():
    print("hello")
    conn = mysql.connector.connect(**config)
    print("Connection established")
    cursor = conn.cursor()
    # Read data
    cursor.execute("SELECT * FROM earthquakedata;")
    rows = cursor.fetchall()
    print("Read",cursor.rowcount,"row(s) of data.")

    # Print all rows
    for row in rows:
        print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

  # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print('Done!!!')

    return render_template('assign3.html')

if __name__ == '__main__':
  app.run()

