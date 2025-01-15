
import matplotlib.pyplot as plt
import cv2

def findBorderBox(results,model):
    try:
        all_boxes = []  # เก็บพิกัดของทุกกรอบ
        
        for result in results:
            for box in result.boxes:
                # พิกัดกรอบในรูปแบบ [x1, y1, x2, y2]
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # ดึงชื่อคลาสจาก index
                class_index = int(box.cls[0])  # ต้องแปลงเป็น int ก่อน
                class_name = model.names[class_index]  # ดึงชื่อคลาส
                
                # เก็บพิกัดเป็น int ใน all_boxes
                all_boxes.append((int(x1), int(y1), int(x2), int(y2)))
        
        return all_boxes
    except Exception as e:
        print(e)