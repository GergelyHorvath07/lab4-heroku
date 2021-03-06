from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os 
import requests

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

@app.route("/api/bot", methods = ['POST'])
def bot():
        webhookMessage = request.json
        print(webhookMessage)
        messageId = webhookMessage["data"]["id"]
        print(messageId)

        url = "https://api.ciscospark.com/v1/messages/" + messageId
        r = requests.get(url, headers={'Authorization': 'Bearer NjAzMzljMTItZTZiOS00YWFjLWI5ZGMtYmFhOWNmZTQwOWJmMmQ2ODFhYmUtMDJh_PF84_consumer'})
        print(r.json())
        message = r.json()["text"]
        print(message)

        mentionedPeopleId = webhookMessage["data"]["mentionedPeople"][0]
        print(mentionedPeopleId)
        if mentionedPeopleId == "Y2lzY29zcGFyazovL3VzL1BFT1BMRS81OGE1ZjYwZC05NGZlLTQ4ODItOWMwYi05Yzk1MmQ0ZDg1ZjQ":
                roomId = r.json()["roomId"]
                url = "https://api.ciscospark.com/v1/messages"
                r = requests.post(url, headers={'Authorization': 'Bearer NjAzMzljMTItZTZiOS00YWFjLWI5ZGMtYmFhOWNmZTQwOWJmMmQ2ODFhYmUtMDJh_PF84_consumer'}, data={'roomId': roomId, 'text': 'Hello from your bot!'})
        return jsonify(webhookMessage)
        
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