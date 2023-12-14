from flask import Flask, render_template, request
import py.tim_predict as tp

# 画像ファイルのアップロード処理
def uploader():
    global f
    f = request.files.get("image")
    
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def upload_file():
    
        # 開始を押した時の処理
        uploader()
        tp.do_check(f)
        result = tp.result
        auth_probability = tp.auth_probability
        return render_template("result.html",result=result,auth_probability=auth_probability)



if __name__ == "__main__":

    app.run(debug=True,host='192.168.1.108', port=50002)
