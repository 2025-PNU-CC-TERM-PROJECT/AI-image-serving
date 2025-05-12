from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import tempfile
import os
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions


app = FastAPI()
model = VGG16(weights='imagenet')

@app.post("/img")
async def img(file: UploadFile = File(...)):
    try:
        # 1. 임시 파일 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # 2. PIL로 열기
        pil_img = Image.open(tmp_path).convert("RGB")

        # 3. 정사각형 crop + resize
        w, h = pil_img.size
        s = min(w, h)
        x, y = (w - s) // 2, (h - s) // 2
        cropped = pil_img.crop((x, y, x + s, y + s)).resize((224, 224))

        # 4. 벡터화 + 전처리
        img_array = image.img_to_array(cropped)
        img_batch = np.expand_dims(img_array, axis=0)
        preprocessed = preprocess_input(img_batch)

        # 5. 예측
        preds = model.predict(preprocessed)
        top_preds = decode_predictions(preds, top=5)[0]  # top 5 결과 추출

        # 6. 응답 형식 정리
        result = [
            {"class": pred[1], "confidence": float(pred[2])}
            for pred in top_preds
        ]

        # 7. 파일 삭제
        os.remove(tmp_path)

        return JSONResponse(content={"predictions": result})

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})
