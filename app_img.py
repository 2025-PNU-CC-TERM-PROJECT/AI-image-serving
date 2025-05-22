from kserve import Model
from kserve import ModelServer
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
import base64
import io

class MobileNetModel(Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.model = None

    def load(self):
        self.model = MobileNetV2(weights='imagenet')  # ✅ 모델 일치
        self.ready = True
        return self

    def predict(self, request: dict, context: dict = None) -> dict:
        try:
            img_base64 = request["instances"][0]["b64"]
            img_bytes = base64.b64decode(img_base64)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            w, h = img.size
            s = min(w, h)
            x, y = (w - s) // 2, (h - s) // 2
            cropped = img.crop((x, y, x + s, y + s)).resize((224, 224))
            img_array = image.img_to_array(cropped)
            img_batch = np.expand_dims(img_array, axis=0)
            preprocessed = preprocess_input(img_batch)
            preds = self.model.predict(preprocessed)
            top_preds = decode_predictions(preds, top=5)[0]
            return {"predictions": [{"class": c[1], "confidence": float(c[2])} for c in top_preds]}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    model = MobileNetModel("mobilenet")
    model.load()
    ModelServer().start([model])
