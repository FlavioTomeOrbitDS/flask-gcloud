from flask import Flask, render_template, request, Response
import requests
import pandas as pd
from io import BytesIO
from time import sleep
from datetime import datetime
from scripts import getTweetsFullArchive,getTweetsCount,formatDates, getTweetsRecentCount, getRecentTweets

app = Flask(__name__)


#----------------- Views Methods ---------------------------------

@app.route("/tweetscount", methods=['GET', 'POST'])
def tweetscount():
    if request.method == "GET":
        print("Testando")
        return render_template('tweetscount.html')
    else:
        q = request.form["query"]
        lang = request.form['idioma']
        dt1 = request.form['datepicker']
        dt2 = request.form['datepicker2']
    
        fromDate, toDate = formatDates(dt1,dt2)                        
        
        #full tweets count:
        df_output = getTweetsCount(q,lang, fromDate, toDate)
       
        #recent search:
        #df_output = getTweetsRecentCount(q, lang)
        
        # export excel file
        buffer = BytesIO()        
        df_output.to_excel(buffer)
        headers = {
             'Content-Disposition': 'attachment; filename=output.xlsx',
             'Content-type': 'application/vnd.ms-excel'
        }
        
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
            
        
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        print("Testando")
        return render_template('index.html')
    else:
        q = request.form["query"]
        lang = request.form['idioma']
        dt1 = request.form['datepicker']
        dt2 = request.form['datepicker2']
    
        fromDate, toDate = formatDates(dt1,dt2)                        
        
        #full search:
        df_output = getTweetsFullArchive(q,lang, fromDate, toDate)
       
        #recent search:
        #df_output = getRecentTweets(q, lang)
        
        # export excel file
        buffer = BytesIO()        
        df_output.to_excel(buffer)
        headers = {
             'Content-Disposition': 'attachment; filename=output.xlsx',
             'Content-type': 'application/vnd.ms-excel'
        }
        
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)