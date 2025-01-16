from flask import jsonify

from services.handleImage import handleImage
from services.cropLicensePlate import cropLicensePlate
from services.yoloRead import yoloRead
import time
def readLicensePlate(request):
    try:
        
        start_time = time.time()
        
        handleImage(request) #save image
        
        #crop image
        crop_result = cropLicensePlate()
        if len(crop_result) == 0:
            return jsonify({'message':"can't detect license plate"})
        
        result = yoloRead()
        
        end_time = time.time()
        process_time = end_time - start_time
        print("time : "+str(process_time))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error":str(e)}), 500