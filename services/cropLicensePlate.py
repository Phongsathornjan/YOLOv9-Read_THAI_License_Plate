from flask import jsonify
from ultralytics import YOLO
import os
import cv2

from services.findBorderBox import findBorderBox

def cropLicensePlate():
    try:
        
        Crop_License_Plate_model = YOLO('../models/YOLO_crop.pt')
        
        image_path = "upload_folder/upload_Photo.jpg"
        original_image = cv2.imread(image_path)
        
        Crop_results = Crop_License_Plate_model.predict(original_image)
        
        all_boxes_plate = findBorderBox(Crop_results, Crop_License_Plate_model)
        
        # ถ้าไม่พบป้ายทะเบียน ให้ซูมเข้าและตรวจจับอีกครั้ง
        if len(all_boxes_plate) == 0:
            scale = 1.2
            h, w = original_image.shape[:2]
            center_x, center_y = w // 2, h // 2
            new_w, new_h = int(w / scale), int(h / scale)

            zoom_image = original_image[center_y - new_h // 2:center_y + new_h // 2,
                            center_x - new_w // 2:center_x + new_w // 2]
            if zoom_image.size == 0:
                print("Error: Cropped image is empty.")
                return []

            original_image = zoom_image
            Crop_results = Crop_License_Plate_model.predict(original_image)
            all_boxes_plate = findBorderBox(Crop_results, Crop_License_Plate_model)
            
            if len(all_boxes_plate) == 0:
                return []
            
        result = []
        # อ่านข้อมูลจากกรอบที่ครอบแต่ละกรอบ
        for i, (x1, y1, x2, y2) in enumerate(all_boxes_plate, start=1):
            
            cropped_image = original_image[y1+5:y2-5, x1+5:x2-5]  # ตัดภาพตามพิกัด
            resized_image = cv2.resize(cropped_image, (400, 400))
            
            result.append({
                "x1": x1,
                "x2": x2,
                "y1": y1,
                "y2": y2
            })
            
            #save cropped and resize img
            cropped_folder = 'cropped_folder'
            os.makedirs(cropped_folder, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี
            file_path = os.path.join(cropped_folder, f"License_plate_{i}.jpg")
            cv2.imwrite(file_path, resized_image)  
               
        return result
    except Exception as e:
        print(e)
        