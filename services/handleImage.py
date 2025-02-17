from flask import jsonify
import os

def handleImage(request):
    try:
        # ตรวจสอบว่า request มีไฟล์
        if 'image' not in request.files:
            return False , {'error' : 'No file part in the request'}
            
        file = request.files['image']
        
        # ตรวจสอบว่าไฟล์มีชื่อ
        if file.filename == '':
            return False , {"error": "No selected file"}
        
        # ตรวจสอบชนิดไฟล์
        allowed_content_types = ['image/jpeg', 'image/png']
        if file.content_type not in allowed_content_types:
            return False , {"error": "File type not allowed. Only JPEG, PNG, GIF images are accepted."}
        
        # บันทึกไฟล์
        upload_folder = 'upload_folder'
        os.makedirs(upload_folder, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี
        file_path = os.path.join(upload_folder, "upload_Photo.jpg")
        file.save(file_path)
        
        return True, {"status" : "success"}
    except Exception as e:
        return jsonify({'error':str(e)}),500