from flask import Flask

app = Flask('tweet')

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
