from flask import Flask, render_template, request, Response
from io import BytesIO
from scripts import *

app = Flask(__name__)

@app.route("/tweetscount", methods=['GET', 'POST'])
def tweetscount():
    if request.method == "GET":
        return render_template('tweetscount.html')
    else:  
        # gets the query params
        q = request.form["query"]     
        
        filename = q+"-"+str(datetime.now())   
        
        # remove retweets
        include_retweets = request.form.get("retweets_chk")
        if include_retweets != '1':
            q = q + " -is:retweet"        
        # remove replies
        include_replies = request.form.get("replies_chk")
        if include_replies != '1':
            q = q + " -is:reply"        
                
        lang = request.form['idioma']
              
        # gets the value from checkbox
        chk = request.form.getlist('chkbox')
        #if value == 0, then do the recent search
        if chk[0] == '1':                    
            df_output = getTweetsRecentCount(q, lang)
        else:
        # full search            
            dt1 = request.form['datepicker']
            dt2 = request.form['datepicker2']    
            fromDate, toDate = formatDates(dt1,dt2)                                            
            df_output = getTweetsCount(q,lang, fromDate, toDate)   
                        
        return exportexcelfile(df_output,filename)
        
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":        
        return render_template('index.html')
    else:
        # get the query params
        q = request.form["query"]
        filename = q+"-"+str(datetime.now())    
        # remove retweets
        include_retweets = request.form.get("retweets_chk")
        if include_retweets != '1':
            q = q + " -is:retweet"        
        # remove replies
        include_replies = request.form.get("replies_chk")
        if include_replies != '1':
            q = q + " -is:reply"        
        
        lang = request.form['idioma']
        # gets the value from checkbox
        chk = request.form.getlist('chkbox')                        
        #if value == 0, then do the recent search
        if chk[0] == '1':                        
            df_output = getRecentTweets(q, lang)
        else:
        # full search            
            dt1 = request.form['datepicker']
            dt2 = request.form['datepicker2']    
            fromDate, toDate = formatDates(dt1,dt2)                                            
            df_output = getTweetsFullArchive(q,lang, fromDate, toDate)   
                        
        return exportexcelfile(df_output,filename)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)