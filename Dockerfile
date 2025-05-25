FROM python:3.10-slim

WORKDIR /app
COPY app_img.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2; MobileNetV2(weights='imagenet')" && \
    rm -rf /root/.cache/pip

CMD ["python", "app_img.py"]