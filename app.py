from flask import Flask, request, Response, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from models import *
from PIL import Image
import base64
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1048576
db_init(app)

ALLOWED_EXTENSIONS = {'png', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def upload_img():
    try:
        img = request.files['img']

        if not img:
            return render_template('home.html', message="Image not added")

        if not allowed_file(img.filename):
            return render_template('home.html', message="Image file should be jpeg or png")

        if img:
            data = img.read()
            img.seek(0, os.SEEK_END)
            size = img.tell()
            resolution = Image.open(img).size
            resolution = str(resolution[0]) + " x " + str(resolution[1])
            filename = secure_filename(img.filename)
            mimetype = img.mimetype
            if not filename or not mimetype:
                return render_template('home.html', message="Bad request")

            img = Img(size=size, resolution=resolution, img=data, name=filename, mimetype=mimetype)
            db.session.add(img)
            db.session.commit()

            img_details = Img.query.all()[-1]

            return redirect(url_for('img_detail', id=img_details.id))
        else:
            return render_template('home.html', message="Img not selected")
    except RequestEntityTooLarge:
        return render_template('home.html', message="Image size too large. Limit is 1 MB.")


@app.route('/links')
def links():
    all_img = Img.query.all()
    if len(all_img) == 0:
        return render_template('home.html', message="No images added.")
    else:
        return render_template('home.html', all_img=all_img)


@app.route('/image/<int:id>')
def img_detail(id):
    try:
        img = Img.query.filter_by(id=id).first()
        image = base64.b64encode(img.img).decode("utf-8")
        return render_template("img_info.html", img=image, image_detail=img)
    except:
        return render_template('img_info.html', message="Image detail doesn't exists.")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
