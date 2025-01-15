from flask import Flask, jsonify
from services.readLicensePlate import readLicensePlate
app = Flask(__name__)

@app.route('/readLicensePlate',methods=['POST'])
def handleReadLicensePlate():
    return readLicensePlate()

if __name__ == '__main__':
    app.run(debug=True)