from flask import Flask, request
from services.readLicensePlate import readLicensePlate
app = Flask(__name__)

@app.route('/readLicensePlate',methods=['POST'])
def handleReadLicensePlate():
    return readLicensePlate(request)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
