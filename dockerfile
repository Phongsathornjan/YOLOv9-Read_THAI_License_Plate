FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# ตั้งค่า environment
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# อัปเดตระบบและติดตั้ง dependencies
RUN apt update && apt install -y \
    software-properties-common \
    python3-pip \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update && apt install -y python3.9 python3.9-venv python3.9-dev python3.9-distutils \
    && apt install -y libgl1 libglib2.0-0 \
    && apt clean

# คัดลอกไฟล์ใน folder ปัจจุบันไปยัง /app ใน image
COPY requirement.txt /app/
COPY . /app

RUN python3.9 -m venv venv  
RUN /app/venv/bin/pip install -r /app/requirement.txt  
RUN /app/venv/bin/pip uninstall -y torch torchvision torchaudio  
RUN /app/venv/bin/pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124


# อนุญาติให้ port 5000 สามารถเข้าถึงได้
EXPOSE 5000

CMD ["/app/venv/bin/python", "app.py"]