from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import io

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return "Select a file", 400

        if not allowed_file(file.filename):
            return "Wrong file type", 400

        filename = secure_filename(file.filename)

        # 메모리에 잠깐 저장 후 바로 다운로드 응답
        data = file.read()
        buf = io.BytesIO(data)
        buf.seek(0)

        # 브라우저가 “파일 다운받으세요” 라고 인식하도록 헤더 설정
        return send_file(
            buf,
            as_attachment=True,
            download_name=filename,
            mimetype=file.mimetype
        )

    return '''
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*">
      <button type="submit">Upload & Download</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
