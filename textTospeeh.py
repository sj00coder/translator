from gtts import gTTS 
import os 
def audiocreater(mytext,language):
    myobj = gTTS(text=mytext, lang=language, slow=False,lang_check=False) 
    myobj.save(os.path.join('static',"welcome23.mp3")) 
