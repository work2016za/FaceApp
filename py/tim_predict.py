import math
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import app

# スクリプトの位置を取得
script_dir = os.path.dirname(os.path.abspath(__file__))

#作成したモデルのロード
model_dir = os.path.join(script_dir, 'model')  
model_path = os.path.join(model_dir, 'model.keras')
model = load_model(model_path)

def preprocess_image(image_path, target_size=(50, 50)):
    # 画像をロード
    img = Image.open(image_path)
    # RGBに変換
    img = img.convert("RGB")
    # リサイズ
    img = img.resize(target_size)
    # numpy配列に変換
    img_array = np.asarray(img)
    # 正規化
    img_array = img_array.astype("float32") / 255.0
    # バッチ次元を追加
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

#ラベル
labels = ["mukuno","not-mukuno"]

#ラベルのネーミング
name_map = {
    "mukuno": "椋野さん",
    "not-mukuno":"椋野さんではない人"
}


# 判定する画像のパス
def do_check(f):
    filename = secure_filename(f.filename)
    #filepath = "py/" + filename
    filepath=filename
    other_filepath = os.path.splitext(filepath)[0] + '.JPG'
    f.save(other_filepath)

    processed_image = preprocess_image(other_filepath)
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions, axis=1)


    #判定
    predicted_label = labels[predicted_class[0]]

    # 確率の取得
    probability = predictions[0][predicted_class[0]]

    # 結果表示
    print("{:.2f}% の確率で {} です。".format(probability * 100, name_map[predicted_label]))
    global result, auth_probability
    result = "{}".format(name_map[predicted_label])
    auth_probability = "{}%".format(math.floor(probability * 100))
    os.remove(other_filepath)

if __name__ == "__main__":
    do_check()