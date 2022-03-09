from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveParcels', methods=['POST'])
def saveParcel():
    data = request.form['parcels-data']

    json_object = json.loads(data)


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')