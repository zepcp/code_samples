"""
Pretrained models: https://pytorch.org/docs/stable/torchvision/models.html
"""
import io
import json

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, request, render_template


app = Flask(__name__)
class_index = json.load(open("class_index.json"))
model = models.densenet121(pretrained=True)
model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return class_index[predicted_idx]


@app.route("/predict", methods=["GET"])
def predict_get():
    return render_template("upload.html")


@app.route("/predict", methods=["POST"])
def predict_post():
    file = request.files.get("image")
    class_id, class_name = get_prediction(image_bytes=file.read())
    return {"class_id": class_id, "class_name": class_name}


if __name__ == '__main__':
    app.run(debug=True)
