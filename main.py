from flask import Flask, render_template, request, Response, flash, redirect, url_for, session
from io import BytesIO
from scripts import *

app = Flask(__name__)

app.secret_key = "myscrtky"

user = {"username": "@orbitdatascience", "password":"psswd@0123"}

languages = {
    "pt": "Portuguese",
    "en": "English",
    "en-gb": "English UK",
    "es": "Spanish",
    "fr": "French",    
    "ar": "Arabic",
    "ja": "Japanese",    
    "de": "German",
    "it": "Italian",
    "id": "Indonesian",    
    "ko": "Korean",
    "tr": "Turkish",
    "ru": "Russian",
    "nl": "Dutch",
    "fil": "Filipino",
    "msa": "Malay",
    "zh-tw": "Traditional Chinese",
    "zh-cn": "Simplified Chinese",
    "hi": "Hindi",
    "no": "Norwegian",
    "sv": "Swedish",
    "fi": "Finnish",
    "da": "Danish",
    "pl": "Polish",
    "hu": "Hungarian",
    "fa": "Farsi",
    "he": "Hebrew",
    "ur": "Urdu",
    "th": "Thai"   
  }

countries = { 
  "BR": "Brazil",
  "GB": "United Kingdom",
  "US": "United States",
  "AF": "Afghanistan",
  "AX": "Aland Islands",
  "AL": "Albania",
  "DZ": "Algeria",
  "AS": "American Samoa",
  "AD": "Andorra",
  "AO": "Angola",
  "AI": "Anguilla",
  "AQ": "Antarctica",
  "AG": "Antigua And Barbuda",
  "AR": "Argentina",
  "AM": "Armenia",
  "AW": "Aruba",
  "AU": "Australia",
  "AT": "Austria",
  "AZ": "Azerbaijan",
  "BS": "Bahamas",
  "BH": "Bahrain",
  "BD": "Bangladesh",
  "BB": "Barbados",
  "BY": "Belarus",
  "BE": "Belgium",
  "BZ": "Belize",
  "BJ": "Benin",
  "BM": "Bermuda",
  "BT": "Bhutan",
  "BO": "Bolivia",
  "BA": "Bosnia And Herzegovina",
  "BW": "Botswana",
  "BV": "Bouvet Island",
  "IO": "British Indian Ocean Territory",
  "BN": "Brunei Darussalam",
  "BG": "Bulgaria",
  "BF": "Burkina Faso",
  "BI": "Burundi",
  "KH": "Cambodia",
  "CM": "Cameroon",
  "CA": "Canada",
  "CV": "Cape Verde",
  "KY": "Cayman Islands",
  "CF": "Central African Republic",
  "TD": "Chad",
  "CL": "Chile",
  "CN": "China",
  "CX": "Christmas Island",
  "CC": "Cocos (Keeling) Islands",
  "CO": "Colombia",
  "KM": "Comoros",
  "CG": "Congo",
  "CD": "Congo, Democratic Republic",
  "CK": "Cook Islands",
  "CR": "Costa Rica",
  "CI": "Cote D\"Ivoire",
  "HR": "Croatia",
  "CU": "Cuba",
  "CY": "Cyprus",
  "CZ": "Czech Republic",
  "DK": "Denmark",
  "DJ": "Djibouti",
  "DM": "Dominica",
  "DO": "Dominican Republic",
  "EC": "Ecuador",
  "EG": "Egypt",
  "SV": "El Salvador",
  "GQ": "Equatorial Guinea",
  "ER": "Eritrea",
  "EE": "Estonia",
  "ET": "Ethiopia",
  "FK": "Falkland Islands (Malvinas)",
  "FO": "Faroe Islands",
  "FJ": "Fiji",
  "FI": "Finland",
  "FR": "France",
  "GF": "French Guiana",
  "PF": "French Polynesia",
  "TF": "French Southern Territories",
  "GA": "Gabon",
  "GM": "Gambia",
  "GE": "Georgia",
  "DE": "Germany",
  "GH": "Ghana",
  "GI": "Gibraltar",
  "GR": "Greece",
  "GL": "Greenland",
  "GD": "Grenada",
  "GP": "Guadeloupe",
  "GU": "Guam",
  "GT": "Guatemala",
  "GG": "Guernsey",
  "GN": "Guinea",
  "GW": "Guinea-Bissau",
  "GY": "Guyana",
  "HT": "Haiti",
  "HM": "Heard Island & Mcdonald Islands",
  "VA": "Holy See (Vatican City State)",
  "HN": "Honduras",
  "HK": "Hong Kong",
  "HU": "Hungary",
  "IS": "Iceland",
  "IN": "India",
  "ID": "Indonesia",
  "IR": "Iran, Islamic Republic Of",
  "IQ": "Iraq",
  "IE": "Ireland",
  "IM": "Isle Of Man",
  "IL": "Israel",
  "IT": "Italy",
  "JM": "Jamaica",
  "JP": "Japan",
  "JE": "Jersey",
  "JO": "Jordan",
  "KZ": "Kazakhstan",
  "KE": "Kenya",
  "KI": "Kiribati",
  "KR": "Korea",
  "KP": "North Korea",
  "KW": "Kuwait",
  "KG": "Kyrgyzstan",
  "LA": "Lao People\"s Democratic Republic",
  "LV": "Latvia",
  "LB": "Lebanon",
  "LS": "Lesotho",
  "LR": "Liberia",
  "LY": "Libyan Arab Jamahiriya",
  "LI": "Liechtenstein",
  "LT": "Lithuania",
  "LU": "Luxembourg",
  "MO": "Macao",
  "MK": "Macedonia",
  "MG": "Madagascar",
  "MW": "Malawi",
  "MY": "Malaysia",
  "MV": "Maldives",
  "ML": "Mali",
  "MT": "Malta",
  "MH": "Marshall Islands",
  "MQ": "Martinique",
  "MR": "Mauritania",
  "MU": "Mauritius",
  "YT": "Mayotte",
  "MX": "Mexico",
  "FM": "Micronesia, Federated States Of",
  "MD": "Moldova",
  "MC": "Monaco",
  "MN": "Mongolia",
  "ME": "Montenegro",
  "MS": "Montserrat",
  "MA": "Morocco",
  "MZ": "Mozambique",
  "MM": "Myanmar",
  "NA": "Namibia",
  "NR": "Nauru",
  "NP": "Nepal",
  "NL": "Netherlands",
  "AN": "Netherlands Antilles",
  "NC": "New Caledonia",
  "NZ": "New Zealand",
  "NI": "Nicaragua",
  "NE": "Niger",
  "NG": "Nigeria",
  "NU": "Niue",
  "NF": "Norfolk Island",
  "MP": "Northern Mariana Islands",
  "NO": "Norway",
  "OM": "Oman",
  "PK": "Pakistan",
  "PW": "Palau",
  "PS": "Palestinian Territory, Occupied",
  "PA": "Panama",
  "PG": "Papua New Guinea",
  "PY": "Paraguay",
  "PE": "Peru",
  "PH": "Philippines",
  "PN": "Pitcairn",
  "PL": "Poland",
  "PT": "Portugal",
  "PR": "Puerto Rico",
  "QA": "Qatar",
  "RE": "Reunion",
  "RO": "Romania",
  "RU": "Russian Federation",
  "RW": "Rwanda",
  "BL": "Saint Barthelemy",
  "SH": "Saint Helena",
  "KN": "Saint Kitts And Nevis",
  "LC": "Saint Lucia",
  "MF": "Saint Martin",
  "PM": "Saint Pierre And Miquelon",
  "VC": "Saint Vincent And Grenadines",
  "WS": "Samoa",
  "SM": "San Marino",
  "ST": "Sao Tome And Principe",
  "SA": "Saudi Arabia",
  "SN": "Senegal",
  "RS": "Serbia",
  "SC": "Seychelles",
  "SL": "Sierra Leone",
  "SG": "Singapore",
  "SK": "Slovakia",
  "SI": "Slovenia",
  "SB": "Solomon Islands",
  "SO": "Somalia",
  "ZA": "South Africa",
  "GS": "South Georgia And Sandwich Isl.",
  "ES": "Spain",
  "LK": "Sri Lanka",
  "SD": "Sudan",
  "SR": "Suriname",
  "SJ": "Svalbard And Jan Mayen",
  "SZ": "Swaziland",
  "SE": "Sweden",
  "CH": "Switzerland",
  "SY": "Syrian Arab Republic",
  "TW": "Taiwan",
  "TJ": "Tajikistan",
  "TZ": "Tanzania",
  "TH": "Thailand",
  "TL": "Timor-Leste",
  "TG": "Togo",
  "TK": "Tokelau",
  "TO": "Tonga",
  "TT": "Trinidad And Tobago",
  "TN": "Tunisia",
  "TR": "Turkey",
  "TM": "Turkmenistan",
  "TC": "Turks And Caicos Islands",
  "TV": "Tuvalu",
  "UG": "Uganda",
  "UA": "Ukraine",
  "AE": "United Arab Emirates",
  "UM": "United States Outlying Islands",
  "UY": "Uruguay",
  "UZ": "Uzbekistan",
  "VU": "Vanuatu",
  "VE": "Venezuela",
  "VN": "Vietnam",
  "VG": "Virgin Islands, British",
  "VI": "Virgin Islands, U.S.",
  "WF": "Wallis And Futuna",
  "EH": "Western Sahara",
  "YE": "Yemen",
  "ZM": "Zambia",
  "ZW": "Zimbabwe"
}

def verifica_datas(dt1, dt2):
   # Verify the dates informed by user
    print('verificando datas!')
    current_date = datetime.now()
    current_date_str = current_date.strftime("%d/%m/%Y")
    if compare_dates(dt1,current_date_str) == 'later' :                                        
        flash('Atenção! A o parâmetro Data Inicial é maior que a Data Atual.')               
        #return render_template('index.html') 
        return 0
    if compare_dates(dt1,dt2) == 'later':
        flash('Atenção! A o parâmetro Data Final é maior que a Data Inicial.')               
        #return render_template('index.html')  
        return 0
    
    return 1

#-------------------------------------- TWEETS COUNT -------------------------------------------
@app.route("/tweetscount", methods=['GET', 'POST'])
def tweetscount():
    if('user' in session and session['user'] == user['username']):        
        if request.method == "GET":
            return render_template('tweetscount.html', countries = countries, languages = languages)
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
            
            country = request.form['country_input']
            
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
                    return render_template('tweetscount.html')
                
                if verifica_datas(dt1,dt2)==0:
                   return render_template('tweetscount.html')              
               
                df_output = getTweetsRecentCount(q, lang, fromDate, toDate)
            else:
            # full search                        
                include_geo = request.form.get("coordinates_chk")
                if include_geo == '1':
                    print("usando coordenadaas")
                    lat = request.form['lat_input']
                    long = request.form['long_input']
                    radius = request.form['radius_input']
                else:
                    print("Sem usar coord")
                    lat='-1'                                                             
                    long="-1"
                    radius="-1"
                    
                fromDate, toDate = formatDates(dt1,dt2,'full')  
                
                if verifica_datas(dt1,dt2)==0:
                   return render_template('tweetscount.html')  
                           
                df_output = getTweetsCount(q,lang, fromDate, toDate,lat,long,radius,country)   
                            
            return exportexcelfile(df_output,filename)            
    else:
        # user not logged
        flash('É necessário fazer o login!')               
        return render_template('login.html')        

#-------------------------------------- TWEETS SEARCH -------------------------------------------        
@app.route("/", methods=['GET', 'POST'])
def index():
    # login
    if('user' in session and session['user'] == user['username']):        
        if request.method == "GET":         
            return render_template('index.html',countries = countries, languages = languages)
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
            
            country = request.form['country_input']
            
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
                
                if verifica_datas(dt1,dt2)==0:
                   return render_template('index.html')  
                
                
                # elif dt2 > currentDate.strftime("%d/%m/%Y"):
                #     flash('Atenção! A o parâmetro Data Final é maior que a Data Atual.')               
                #     return render_template('index.html')            
                                                            
                df_output = getRecentTweets(q, lang,fromDate,toDate)            
            else:
            # full search                        
                include_geo = request.form.get("coordinates_chk")
                if include_geo == '1':
                    print("usando coordenadaas")
                    lat = request.form['lat_input']
                    long = request.form['long_input']
                    radius = request.form['radius_input']
                else:
                    print("Sem usar coord")
                    lat='-1'                                                             
                    long="-1"
                    radius="-1"
                
                fromDate, toDate = formatDates(dt1,dt2,'full')                                            
                
                if verifica_datas(dt1,dt2)==0:
                   return render_template('index.html')  
                
                df_output = getTweetsFullArchive(q,lang, fromDate, toDate,lat,long,radius,country)   
                            
            return exportexcelfile(df_output,filename)
            #return render_template('index.html') 
    else:
        # user not logged
        flash('É necessário fazer o login!')               
        return render_template('login.html')
        
    
@app.route("/login", methods = ['POST','GET'])
def login():
   session.permanent = False
   if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == user['username'] and password == user['password']:            
            session['user'] = username
            return redirect('/')
        else:
            flash('Login não cadastrado!')               
            return render_template('login.html')
    
   return render_template("login.html") 

@app.route("/logout", methods = ['POST','GET'])
def logout():
    session.pop('user')         
    return redirect('/login')
    
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)