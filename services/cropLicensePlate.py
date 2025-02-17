from ultralytics import YOLO
import os
import cv2

from services.findBorderBox import findBorderBox
from services.PerspectiveTransform import PerspectiveTransform

def cropLicensePlate():
    try:
        current_directory = os.getcwd()
        
        Crop_License_Plate_model = YOLO(os.path.join(current_directory, 'models', 'YOLO_crop.pt'))
        Crop_letter_model = YOLO(os.path.join(current_directory, 'models', 'YOLO_read.pt'))
        
        image_path = "upload_folder/upload_Photo.jpg"
        original_image = cv2.imread(image_path)
        if original_image is None:
            return False , {'error':e, f'message' : "can't rear image at {image_path}"} , {'error': 'can\'t detect license plate'}
        
        Crop_results = Crop_License_Plate_model.predict(original_image,device=0)
        
        all_boxes_plate = findBorderBox(Crop_results, Crop_License_Plate_model)
        
        if len(all_boxes_plate) == 0:
            
            if len(all_boxes_plate) == 0:
                return False , {'message':"can't detect license plate"} , {'error': 'can\'t detect license plate'}
            
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
            
            cropped_xy = [y1, y2, x1, x2]
            letter_results = Crop_letter_model.predict(resized_image,device=0)
            all_letter_boxes = findBorderBox(letter_results, Crop_letter_model)
            if len(all_letter_boxes) == 0:
               break
            all_letter_boxes.sort(key=lambda box: (box[0], box[1]))  # เรียงตาม x1 และ y1 
            xx1 = all_letter_boxes[0][0] - 10
            yy1 = all_letter_boxes[0][1] - 10
            xx2 = all_letter_boxes[len(all_letter_boxes)-1][2]+10
            yy2 = all_letter_boxes[len(all_letter_boxes)-1][1]-10
            if abs(yy1 - yy2) <= 55:
                per_img = resized_image
            elif yy1 > yy2:
                dif = yy1 - yy2    
                per_img = PerspectiveTransform(image_path, cropped_xy, xx1, yy1, xx2, yy2 - 20, xx1, 400, xx2, 400 - dif - 20)
            else:
                dif = yy2 - yy1
                per_img = PerspectiveTransform(image_path, cropped_xy, xx1, yy1 - 20, xx2, yy2, xx1, 400 - dif - 20, xx2, 400)
            
            gray = cv2.cvtColor(per_img, cv2.COLOR_BGR2GRAY)
            eq = cv2.equalizeHist(gray)
            
            #save cropped and resize img
            cropped_folder = 'cropped_folder'
            os.makedirs(cropped_folder, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี
            file_path = os.path.join(cropped_folder, f"License_plate_{i}.jpg")
            cv2.imwrite(file_path, eq)  
        
        return True , {'status':"detected"} , result
    except Exception as e:
        return False , {'error':e} , {'error': 'can\'t detect license plate'}
        