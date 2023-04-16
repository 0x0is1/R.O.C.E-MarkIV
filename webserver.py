from flask import Flask
from threading import Thread

app = Flask('HTTPServer')
@app.route('/')
def home():
    return "Server: Online"

def run():
  app.run(host='0.0.0.0',port=8899)

def start_server():
    t = Thread(target=run)
    t.start()
