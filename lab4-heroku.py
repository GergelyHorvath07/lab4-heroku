from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os 

app = Flask(__name__)

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')

@app.route("/")
def index():
        return app.send_static_file('index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static_dir(path):
        return send_from_directory(static_file_dir, path)

@app.route("/api/helloworld")
def hello():
    return "Hello world!"

@app.route("/api/about", methods = ['POST', 'GET'])
def about():
    global name, age
    if request.method == 'GET':    
        return fetchDataFromDatabase()
    elif request.method == 'POST':
        r = request.json
        name = r["name"]
        age = r['age']
        pushDataToDatabase(name, age)
        return jsonify(name = name, age = age)

def initDatabase():
    conn = sqlite3.connect('about.db') 
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY, name VARCHAR(100), age INTEGER)")
    conn.commit()

def fetchDataFromDatabase():
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM person ORDER BY id DESC;").fetchone()
        return jsonify(id = result[0], name = result[1], age = result[2])

def pushDataToDatabase(name, age):
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        sql = f"INSERT INTO person (name, age) VALUES ('{name}',{age});"
        cur.execute(sql)
        conn.commit()

initDatabase()
pushDataToDatabase("Ödön", 29)
if __name__=="__main__":
    app.run()