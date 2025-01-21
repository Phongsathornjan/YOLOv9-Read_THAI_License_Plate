from flask import jsonify

from services.handleImage import handleImage
from services.cropLicensePlate import cropLicensePlate
from services.yoloRead import yoloRead
import time
def readLicensePlate(request):
    try:
    
        handleImage(request) #save image
        
        #crop image
        crop_result = cropLicensePlate()
        if len(crop_result) == 0:
            return jsonify({'message':"can't detect license plate"})
        
        result = yoloRead()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error":str(e)}), 500