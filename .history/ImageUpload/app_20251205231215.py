from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 업로드 폴더 설정
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Valid file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check the file type is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # import a image from the input --- 1) in index.html
        file = request.files.get('file')

        if not file or file.filename == '':
            return "Select a file", 400

        if not allowed_file(file.filename):
            return "Wrong file type: only 'png', 'jpg', 'jpeg', 'gif' are valid", 400

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # 업로드 후 그 이미지를 다시 화면에 보여줌
        img_url = url_for('static', filename=f'uploads/{filename}')
        return render_template('index.html', img_url=img_url)

    # GET 요청일 때는 기본 페이지
    return render_template('index.html', img_url=None)

if __name__ == '__main__':
    app.run(debug=True)
