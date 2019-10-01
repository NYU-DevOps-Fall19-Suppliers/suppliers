from flask import Flask

server = Flask(__name__)

@server.route('/')
def index():
    return "Welcome to supplier team!"

if __name__ == '__main__':
    server.run()
