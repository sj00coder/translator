from flask import Flask, render_template,request,redirect,url_for,flash,abort,send_file
from translate import Translator
from englisttohindi.englisttohindi import EngtoHindi 
from lang import lang
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = 'downloads'
def count_words(filepath):
   with open(filepath) as f:
       data = f.read()
       data.replace(",", " ")
       return data
def createfile(data):
    with open(os.path.join(app.config['DOWNLOAD_FOLDER'], "download.txt"),"w",encoding="utf-8") as f:

        f.write(data)
    

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST' and request.form["trans"] != "":
        if 'language23' not in request.form or request.form["language23"] == "":
            return render_template('index.html',translation = "Please Enter the language")
        language = request.form["language23"].title()
        if language not in lang:
            return render_template('index.html',translation="SORRY WE CAN'T TRANSLATE IN THIS LANGUAGE TRY ANOTHER ")
            
        elif language == "Hindi":
            
            translation = EngtoHindi(request.form["trans"]).convert
            createfile(translation)
            return render_template('index.html',translation=translation)
        
        else:
            langto = lang[language]
            translator = Translator(to_lang=langto)
            translation= translator.translate(request.form["trans"])
            createfile(translation)
            return render_template('index.html',translation=translation)
    
    elif request.method  == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return render_template('index.html',translation = "PLEASE ENTER A TEXT FILE")
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tobeTranslated = str(count_words(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            if 'language23' not in request.form or request.form["language23"] == "":
                return render_template('index.html',translation = "Please Enter the language")
            language = request.form["language23"].title()
            if language not in lang:
                return render_template('index.html',translation="SORRY WE CAN'T TRANSLATE IN THIS LANGUAGE TRY ANOTHER ")
                
            elif language == "Hindi":
                
                translation = EngtoHindi(tobeTranslated).convert
                createfile(translation)
                return render_template('index.html',translation=translation)
            
            else:
                langto = lang[language]
                translator = Translator(to_lang=langto)
                translation= translator.translate(tobeTranslated)
                createfile(translation)
                return render_template('index.html',translation=translation) 

    return render_template("index.html")
@app.route('/download')
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = os.path.join(app.config['DOWNLOAD_FOLDER'], "download.txt")
    return send_file(path, as_attachment=True, cache_timeout=0)

if __name__ == "__main__":
    app.run(debug=True)