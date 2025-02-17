from flask import jsonify
import os
from services.handleImage import handleImage
from services.cropLicensePlate import cropLicensePlate
from services.yoloRead import yoloRead

def readLicensePlate(request):
    try:
    
        result, e = handleImage(request) #save image
        if(not result):
            return jsonify(e),400
        
        #crop image
        crop_result , error , coordinates = cropLicensePlate()
        
        #ไม่พบป้ายทะเบียน
        if not crop_result:
            os.remove(os.path.join('upload_folder', 'upload_Photo.jpg'))
            return jsonify(error), 200
        
        result = yoloRead()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error":str(e)}), 500