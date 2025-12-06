from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Valid file type
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Save path
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check the file type(extensions)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Run the page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        # Empty file or file is not selected
        if not file or file.filename == '':
            return "No file selected", 400

        # Wong file type (extensions)
        if not allowed_file(file.filename):
            return "Wrong file type: only valid 'png', 'jpg', 'jpeg', 'gif'", 400

        # Confrim the filename
        filename = secure_filename(file.filename)

        # Save path (static/uploads/filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # save the file at disk
        file.save(save_path)

        # 브라우저에서 접근 가능한 URL 만들기
        img_url = url_for('static', filename=f'uploads/{filename}')

        # 페이지에 이미지도 보여주고, 같은 URL로 다운로드도 할 수 있게 넘겨줌
        return render_template('index.html', img_url=img_url)

    # GET 요청: 처음 들어왔을 때
    return render_template('index.html', img_url=None)


if __name__ == '__main__':
    app.run(debug=True)
