from ultralytics import YOLO
import os

from services.matchLabel.map_label import map_label
from services.matchLabel.map_province import map_province

def yoloRead():
    try:
        result = []
        read_license_model = YOLO('../models/YOLO_read.pt',device=0)
        
        #loop in cropped folder
        cropped_folder = 'cropped_folder'
        for i, filename in enumerate(os.listdir(cropped_folder)):
            
            #load image path
            image_path = os.path.join(cropped_folder, filename)
            
            #use YOLO_read model
            results = read_license_model(image_path)
            
            #handle result
            
            # ใช้ list เพื่อเก็บข้อมูล box ทั้งหมดของตัวอักษร
            xy = []
            
            #ถ้าไม่เจอตัวอักษร
            if len(results[0].boxes.xyxy) == 0:
                return []
            
            #ถ้าเจอตัวอักษร
            haveProvince = 0  #detect เจอกี่จังหวัด
            provinceData = [] #เก็บข้อมูลจังหวัดทั้งหมดที่ detect เจอ
            
            index = 0
            for box in results[0].boxes:
                # ดึงข้อมูลของ bounding box
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                # ดึง index ของ class
                class_index = int(box.cls[0])
                class_name = read_license_model.names[class_index]  # ดึงชื่อคลาสจาก model
                    
                # ความมั่นใจ
                confidence = float(box.conf[0]) 
                    
                # แปลงชื่อคลาส
                if class_name.isalpha():  # ตรวจสอบว่าเป็นตัวอักษรล้วน (เป็นจังหวัดไหม)
                    thai_char = map_province(class_name)  # แปลง label เป็นชื่อจังหวัด
                    haveProvince += 1
                    # เพิ่มข้อมูล จังหวัด ลงใน list
                    provinceData.append({
                    "class_name": thai_char,
                    "confidence": confidence,
                    "index" : index
                    })
                else:
                    thai_char = map_label(class_name)  # แปลง label เป็นพยัญชนะ
                    

                # เพิ่มข้อมูล พยัญชนะ ลงใน list
                xy.append({
                    "coordinates": [x1, y1, x2, y2],
                    "class_name": thai_char,
                    "confidence": confidence
                })
                index += 1
                
            #ถ้า detect เจอ 1 จังหวัด
            if haveProvince == 1:
                sorted_boxes_byy1 = sorted(xy, key=lambda ob: ob["coordinates"][1])  # ใช้ y1
                province = sorted_boxes_byy1[len(sorted_boxes_byy1)-1]
                sorted_boxes_byy1.pop(len(sorted_boxes_byy1)-1)
                sorted_boxes_byx1 = sorted(sorted_boxes_byy1, key=lambda ob: ob["coordinates"][0])  # ใช้ x1
            
            #ถ้า detect จังหวัดไม่เจอ
            elif haveProvince == 0:
                sorted_boxes_byy1 = sorted(xy, key=lambda ob: ob["coordinates"][1])  # ใช้ y1
                province = {"class_name":"can't detect"}
                sorted_boxes_byx1 = sorted(sorted_boxes_byy1, key=lambda ob: ob["coordinates"][0])  # ใช้ x1
            
            #ถ้า detect จังหวัดเจอมากกว่า 2   
            else:
                #เลือกจังหวัดที่ confidence มากที่สุด
                province = provinceData[0]
                for o in provinceData[1:]:
                    if province['confidence'] < o['confidence']:
                        province = o

                # ดึง index ที่ต้องการลบจาก provinceData
                indices_to_remove = [item["index"] for item in provinceData]

                # เรียง index จากมากไปน้อย
                indices_to_remove.sort(reverse=True)

                # ลบรายการใน xy ตาม index ที่เรียงไว้
                for index in indices_to_remove:
                    if 0 <= index < len(xy):  # ตรวจสอบว่า index อยู่ในช่วงที่ถูกต้อง
                        xy.pop(index)
                            
                sorted_boxes_byy1 = sorted(xy, key=lambda ob: ob["coordinates"][1])  # ใช้ y1
                sorted_boxes_byx1 = sorted(sorted_boxes_byy1, key=lambda ob: ob["coordinates"][0])  # ใช้ x1
            
            #รวมทุกตัวอักษรเข้าด้วยกัน
            plate_number = ""
            for s in sorted_boxes_byx1:
                plate_number += s["class_name"]
                
            result.append(
                {
                    "detect_id" : i,
                    "plate_number": plate_number,
                    "province": province['class_name']
                    }
                )
        
        os.remove(image_path)
        os.remove(os.path.join('upload_folder', 'upload_Photo.jpg'))
        return result
                
    except Exception as e:
        print(e)