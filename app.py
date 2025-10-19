from flask import Flask, request, redirect, render_template, send_file, url_for, flash
import os
from werkzeug.utils import secure_filename
from crypto_utils import encrypt_file, decrypt_file, list_encrypted_files
from pathlib import Path

UPLOAD_DIR = Path('encrypted_files')
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXT = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'zip'])

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me-in-prod")

def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or f.filename == '':
            flash('No file selected')
            return redirect(request.url)
        filename = secure_filename(f.filename)
        if not allowed(filename):
            flash('File type not allowed. Allowed: ' + ','.join(ALLOWED_EXT))
            return redirect(request.url)
        # save to a temp path then encrypt
        temp_path = Path('tmp') 
        temp_path.mkdir(exist_ok=True)
        temp_file = temp_path / filename
        f.save(str(temp_file))
        # encrypt and remove temp
        encrypted_path = UPLOAD_DIR / (filename + '.enc')
        encrypt_file(str(temp_file), str(encrypted_path))
        temp_file.unlink()
        flash(f'Uploaded and encrypted as {encrypted_path.name}')
        return redirect(url_for('index'))
    files = list_encrypted_files(str(UPLOAD_DIR))
    return render_template('index.html', files=files)

@app.route('/download/<path:enc_name>')
def download(enc_name):
    enc_path = UPLOAD_DIR / enc_name
    if not enc_path.exists():
        flash('File not found')
        return redirect(url_for('index'))
    # decrypt to temp and send
    tmp = Path('tmp')
    tmp.mkdir(exist_ok=True)
    out_path = tmp / enc_name.replace('.enc','')
    decrypt_file(str(enc_path), str(out_path))
    return send_file(str(out_path), as_attachment=True, attachment_filename=out_path.name)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
