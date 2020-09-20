# doing necessary imports
from flask import Flask, render_template, request,jsonify
import requests
import nltk
import urllib
import bs4 as bs
import re 


app = Flask(__name__)  # initialising the flask app with the name 'app'


@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':

        try:
            searchString = request.form['content'].replace(" ","_") 
            url = "https://en.wikipedia.org/wiki/" + searchString
            source = urllib.request.urlopen(url)
            soup = bs.BeautifulSoup(source,'html')

            text = ""
            for para in soup.find_all('p'):
                text = text+para.text

                text = re.sub(r'\n',' ',text)
                text = re.sub(r'\[[0-9]*\]',' ',text)
                text = re.sub(r'\ \' ',' ',text)
                text = text.replace("\'","") 

                # preprocess
                text = text.split('.')
                text =text[0:15]
                text = str(text)
                text = text.replace("', '",".") 
                text =text.replace("['","") 
                text = text.replace("']",".")
            
            
            return render_template('index.html', text=text)
        except:
            return "Woops! No Internet Connection"

    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True) # running the app on the local machine on port 8000