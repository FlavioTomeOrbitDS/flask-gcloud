from flask import Flask, render_template, request, Response, flash
from io import BytesIO
from scripts import *

app = Flask(__name__)

app.secret_key = "super secret key"

#-------------------------------------- TWEETS COUNT -------------------------------------------
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
        
        # get dates
        dt1 = request.form['datepicker']
        dt2 = request.form['datepicker2']    
              
        # gets the value from checkbox
        chk = request.form.getlist('chkbox')
        
        currentDate = datetime.now()
        
        #if value == 0, then do the recent search
        if chk[0] == '1':     
            fromDate, toDate = formatDates(dt1,dt2,'recent')                        
            # Dates vefification
            if getDaysBetweenDates(dt1, currentDate.strftime("%d/%m/%Y")) > 7:
                flash('Atenção! A opção "Recent Search" somente busca tweets dos últimos 7 dias! Verifique a Data Inicial! ')               
                return render_template('index.html')
            elif dt2 > currentDate.strftime("%d/%m/%Y"):
                flash('Atenção! A o parâmetro Data Final é maior que a Data Atual.')               
                return render_template('index.html')                
            df_output = getTweetsRecentCount(q, lang, fromDate, toDate)
        else:
        # full search                        
            fromDate, toDate = formatDates(dt1,dt2,'full')  
            
            if dt2 > currentDate.strftime("%d/%m/%Y"):
                flash('Atenção! A o parâmetro Data Final é maior que a Data Atual.')               
                          
            df_output = getTweetsCount(q,lang, fromDate, toDate)   
                        
        return exportexcelfile(df_output,filename)

#-------------------------------------- TWEETS SEARCH -------------------------------------------        
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":         
        return render_template('index.html')
    else:
        
        # get the query params
        q = request.form["query"]
        filename = q+"-"+str(datetime.now())    
        
        # verufy if remove retweets is checked
        include_retweets = request.form.get("retweets_chk")
        if include_retweets != '1':
            #include the tag in the query
            q = q + " -is:retweet"        
        # verufy if remove replies is checked
        include_replies = request.form.get("replies_chk")
        if include_replies != '1':
            #include the tag in the query
            q = q + " -is:reply"        
        
        lang = request.form['idioma']
        
        # get dates
        dt1 = request.form['datepicker']
        dt2 = request.form['datepicker2']    
        
        # gets the value from checkbox
        chk = request.form.getlist('chkbox')                        
        
        currentDate = datetime.now()
        
        #if value == 0, then do the recent search
        if chk[0] == '1':               
            fromDate, toDate = formatDates(dt1,dt2,'recent')                        
            # Dates vefification
            if getDaysBetweenDates(dt1, currentDate.strftime("%d/%m/%Y")) > 7:
                flash('Atenção! A opção "Recent Search" somente busca tweets dos últimos 7 dias! Verifique a Data Inicial! ')               
                return render_template('index.html')
            elif dt2 > currentDate.strftime("%d/%m/%Y"):
                flash('Atenção! A o parâmetro Data Final é maior que a Data Atual.')               
                return render_template('index.html')            
                                                           
            df_output = getRecentTweets(q, lang,fromDate,toDate)            
        else:
        # full search                        
            fromDate, toDate = formatDates(dt1,dt2,'full')                                            
            
            if dt2 > currentDate.strftime("%d/%m/%Y"):
                flash('Atenção! A o parâmetro Data Final é maior que a Data Atual.')               
                return render_template('index.html')            
            
            df_output = getTweetsFullArchive(q,lang, fromDate, toDate)   
                        
        return exportexcelfile(df_output,filename)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)