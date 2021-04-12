import cloudinary
import cloudinary.uploader
from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["MONGO_DBNAME"] = "gallery"
app.config["MONGO_URI"] = "mongodb://localhost:27017/gallery"

mongo = PyMongo(app)
cloudinary.config(
    cloud_name="CLOUDINARY CLOUD NAME",
    api_key="CLOUDINARY API KEY",
    api_secret="CLOUDINARY API SECRET"
)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery/")
def gallery():
    return render_template("gallery.html", gallery=mongo.db.gallery.find())


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        description = request.form.get("description")
        if image and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            upload_result = cloudinary.uploader.upload(image)
            mongo.db.gallery.insert_one({
                "url": upload_result["secure_url"],
                "description": description.strip()
            })

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
