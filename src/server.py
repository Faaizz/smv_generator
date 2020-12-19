
import os
from collections import OrderedDict

from .main import generate_smv_st

from flask import Flask, request, json, render_template, \
    url_for, redirect, flash, send_from_directory



# create and configure the app
app = Flask(__name__)

# Set secret key
app.config["SECRET_KEY"]= "afcjflnvfdljnvorifnlixd"

# Allowed Extensions
ALLOWED_EXTENSIONS = {'json'}
# Upload Folder
FILES_FOLDER= os.getcwd()

# a simple page that says hello
@app.route('/')
def index():
    return render_template(
        "index.html", 
        index_css=url_for("static", filename="index.css"),
        bootstrap_css=url_for("static", filename="bootstrap.min.css"),
        code_img=url_for("static", filename="code.jpg")
        )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/generate", methods=["POST"])
def generate():
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'sipn_json' not in request.files:
            flash('Please select a file')
            return redirect(request.url)

        file = request.files['sipn_json']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # File selected
        if file and allowed_file(file.filename):
            # Read JSON
            # Get file
            f = request.files['sipn_json']
            # Read file
            with f.stream as f_str:
                input_dict= json.load(f, object_pairs_hook=OrderedDict)

            # Generate amd save SMV
            output_smv= generate_smv_st.smv(input_dict)
            # Write to output file
            with open(os.path.join(FILES_FOLDER, "output.smv"), "w") as f:
                f.write(output_smv)


            # Generate amd save ST
            output_st= generate_smv_st.st(input_dict)
            # Write to output file
            with open(os.path.join(FILES_FOLDER, "output.st"), "w") as f:
                f.write(output_st)

            # Return results page
            return render_template(
                "results.html", 
                index_css=url_for("static", filename="index.css"),
                bootstrap_css=url_for("static", filename="bootstrap.min.css"),
                code_img=url_for("static", filename="code.jpg"),
                output_smv= url_for(".download_file", filename="/output.smv"),
                output_st= url_for(".download_file", filename="/output.st")
                )


# FILE DOWNLOAD
@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(FILES_FOLDER, filename)


# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template(
        'error.html',
        bootstrap_css=url_for("static", filename="bootstrap.min.css"),
        home_page=url_for(".index"),
        err_code= 404,
        err_msg= str(e)
        ), 404

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template(
        'error.html',
        bootstrap_css=url_for("static", filename="bootstrap.min.css"),
        home_page=url_for(".index"),
        err_code= 500,
        err_msg= str(e)
        ), 500

@app.errorhandler(405)
def method_not_allowed(e):
    # note that we set the 405 status explicitly
    return render_template(
        'error.html',
        bootstrap_css=url_for("static", filename="bootstrap.min.css"),
        home_page=url_for(".index"),
        err_code= 405,
        err_msg= str(e)
        ), 405