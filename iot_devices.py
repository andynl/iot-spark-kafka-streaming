from flask import Flask, request, jsonify
from time import time

app = Flask(__name__)

@app.route('/update-sensor', methods=['POST'])
def update_sensor():
    data = request.json

    temp = data['temp']
    humd = data['humd']

    msg = f'{time()}, {temp}, {humd}'

    with open('data.txt', 'a') as f:
        f.write(msg)
        f.write("\n")

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()