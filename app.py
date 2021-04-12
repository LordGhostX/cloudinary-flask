import os
from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["UPLOAD_FOLDER"] = "static/uploads/"
app.config["MONGO_DBNAME"] = "image-gallery"
app.config["MONGO_URI"] = "mongodb://localhost:27017/image-gallery"

mongo = PyMongo(app)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery/")
def gallery():
    return render_template("index.html")


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            mongo.db.gallery.insert_one({"filename": filename})

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
