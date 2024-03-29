from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, action):
    print(f"the action is {action} and filename is{filename}")
    img= cv2.imread(f"uploads/{filename}")
    match action:
        case"cgray":
            imgprocessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newfilename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", imgprocessed)
            return newfilename
            
        case"cpng":
            newfilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            return newfilename
            
        case"cwebp":
            newfilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            return newfilename
            
        case"cjpg":
            newfilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            return newfilename   
    pass
    


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=[ "GET", "POST"])
def edit():
    if request.method == 'POST':
        action = request.form.get("action")
    
        if 'file' not in request.files:
            flash('No file part')
            return "Error-File donot Exist!"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, action)
            flash(f"The image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
        
   #update_is-coming     
        
        return render_template("index.html")
    



app.run(debug=True, port=5001)
