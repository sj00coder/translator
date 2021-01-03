from flask import Flask, render_template,request,redirect
from translate import Translator
from englisttohindi.englisttohindi import EngtoHindi 
from lang import lang
app = Flask(__name__)


@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        
        if request.form["language23"] == "Hindi":
            
            translation = EngtoHindi(request.form["trans"]).convert
            return render_template('index.html',translation=translation)
        
        else:

            langto = lang[request.form["language23"]]
            translator = Translator(to_lang=langto)
            translation= translator.translate(request.form["trans"])
        
            return render_template('index.html',translation=translation)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)