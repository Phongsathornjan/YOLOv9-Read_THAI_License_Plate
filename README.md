# This project for detect and read thai license plate
use 2 model for detect
* YOLOv8n (crop license plate)

  dataset : https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/dataset/3

  code train (colab) : https://colab.research.google.com/drive/1xjmRJvgy2DhbGcKGS3u68hwtQ1bSURGS?usp=sharing 

* YOLOv9t (read license plate)

  dataset : https://universe.roboflow.com/thai-license-plate-wl3xt/lpr-plate-fiq65-3r8ep-akpt2-f6x28-vgj0i/dataset/1

  code train (colab) : https://colab.research.google.com/drive/1MPPeN7fLC2iqsy5LnPIUxbakRphjV_Vg?usp=sharing

## How to run local
before started. You have to install cuda 12.4 form https://developer.nvidia.com/cuda-toolkit

and cudnn that support cuda 12.4 form https://developer.nvidia.com/cudnn

after cuda and cudnn installaion.then follow these step

step 1.) clone project
``` bash
git init
git clone https://github.com/Phongsathornjan/YOLOv9-Read_THAI_License_Plate.git
```
step 2.) Create python virtual environment
``` bash
#python -m venv <name_of_your_virtual_environment>
python -m venv myenv
```
step 3.) install all necessary package
``` bash
pip install -r /app/requirement.txt  
```
step 4.) uninstall torch torchvision torchaudio  
``` bash
pip uninstall -y torch torchvision torchaudio  
```
step 5.) install torch torchvision torchaudio version cuda support
``` bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```
step 6.) run flask server with your virtual environment
``` bash
#command line
myenv\Scripts\activate
python app.py
```

## How to build image and Run as a container

step 1.) clone project
``` bash
git init
git clone https://github.com/Phongsathornjan/YOLOv9-Read_THAI_License_Plate.git
```
step 2.) build image with dockerfile
``` bash
docker build -t license-plate-recognition .
```
step 3.) after build image. Then run you image as a container with gpu access
``` bash
docker run --gpus all -p 5000:5000 license-plate-recognition
```

## API Document (Flask)
#### Endpoint
POST http://127.0.0.1:5000/readLicensePlate

#### Description
API นี้ใช้สำหรับอัปโหลดรูปภาพป้ายทะเบียนรถ และดึงข้อมูลป้ายทะเบียนจากภาพ
<br>

![image](https://github.com/user-attachments/assets/452868c2-25fd-4dbc-96ed-7e48413dda1c)

#### Success Response 200
```JSON
[
    {
        "detect_id": 0,
        "plate_number": "7กก9999",
        "province": "กรุงเทพมหานคร"
    }
]
```
#### bad Response 400
ไม่มีรูปภาพใน image ใน form-data
```JSON
{
    "error": "No selected file"
}
```

ไม่มี key image ใน form data
```JSON
{
    "error": "No selected file"
}
```
JSON response<br>
![image](https://github.com/user-attachments/assets/83b6db81-f486-43e8-9e3a-6183830110b0)


