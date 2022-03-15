from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveParcels', methods=['POST'])
def saveParcel():
    parcels = json.loads(request.form['parcels-data'])
    cuve = json.loads(request.form['cuve-data'])
    json_object = {'parcels': parcels, 'cuve': cuve}

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
