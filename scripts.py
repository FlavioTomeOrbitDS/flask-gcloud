import requests
import pandas as pd
from io import BytesIO
from datetime import datetime
from flask import Response


def compare_dates(date_1, date_2):
    """
    Compare two date strings and return whether date A is equal, earlier, or later than date B.
    
    Args:
        date_a_str (str): A string representing the first date in 'YYYY-MM-DD' format.
        date_b_str (str): A string representing the second date in 'YYYY-MM-DD' format.
    
    Returns:
        str: 'equal' if date A is the same as date B, 'earlier' if date A is earlier than date B, and 'later' if date A is later than date B.
    """
    date_a = datetime.strptime(date_1, "%d/%m/%Y").date()
    date_b = datetime.strptime(date_2, "%d/%m/%Y").date()
    
    if date_a < date_b:
        return 'earlier'
    elif date_a > date_b:
        return 'later'
    else:
        return 'equal'

 # export excel file
def exportexcelfile(df_output, filename):
        buffer = BytesIO()        
        df_output.to_excel(buffer)
        headers = {
             'Content-Disposition': 'attachment; filename={}.xlsx'.format(filename),
             'Content-type': 'application/vnd.ms-excel'
        }
        
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)


def getDaysBetweenDates(date1, date2):
    date_format = "%d/%m/%Y"
    a = datetime.strptime(date1, date_format)
    b = datetime.strptime(date2, date_format)
    
    delta = b - a
    
    return delta.days


#---------------------------------------- FORMAT DATES -----------------------------------------
def formatDates(dt1, dt2, searchtype):
    
    if searchtype == 'full':
        
        dia,mes,ano = dt1.split('/')
        fromDate = ano+mes+dia+"0000"
        
        
        dia,mes,ano = dt2.split('/')
        hour = str(datetime.now().hour)
        if len(hour) < 2:
            hour= '0'+hour
        minute = str(datetime.now().minute)
        if len(minute) < 2:
            minute= '0'+minute
        
        toDate = ano+mes+dia+hour+minute
    else:
        # recent search
        dia,mes,ano = dt1.split('/')
        fromDate = ano+"-"+mes+"-"+dia+"T"+"00:00:00.52Z"
        
        
        dia,mes,ano = dt2.split('/')
        hour = str(datetime.now().hour)
        if len(hour) < 2:
            hour= '0'+hour
        minute = str(datetime.now().minute)
        if len(minute) < 2:
            minute= '0'+minute
        
        toDate = ano+"-"+mes+"-"+dia+"T"+hour+":"+minute+":"+"00.52Z"
        
    return fromDate, toDate

#------------------------------------  GET TWEETS -----------------------------------

def getTweetsFullArchive(query,lang,fromDate, toDate, lat, long, radius,country):
    # use the full archive endpoint from twitter api;
    # fromDate and toDate format: '202208250000'
    
    # max number of requests is 10
    requests_count = 0     
    
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != '-1':
        query = query + ' lang:'+lang
    
    if country != "-1":
        query = query + ' place_country:'+country
        
    # Search using coordinated:  point_radius:[2.355128 48.861118 16km]
    if lat != "-1":
        query = query + " point_radius:["+long+" "+lat+" "+radius+"km]"
        
    # first execution without 'next' param
    params = {'query': query, 'maxResults': '500',
              'fromDate': fromDate, 'toDate': toDate}
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/full.json'
    
    #place_country:BR 
    
    requests_count += 1
    
    response = requests.get(url, headers=header, params=params)
    
    print(response.request.url)
    print(response.request.body)
    print(response.request.headers)
    print("request n.: "+str(requests_count)+" resp code: "+ str(response))
    
    json = response.json()
    try:
        df1 = pd.DataFrame(json['results'])
    except:
        df1 = pd.DataFrame()
        return df1

    # get the next token if exists
    try:
        next_token = json['next']
    except:
        next_token = ' '
        print('no more pages')

    # loop to get response for the endpoint whith next parameter
    while next_token != ' ':        
        
        params = {'query': query, 'maxResults': '500',
                  'fromDate': fromDate, 'toDate': toDate, 'next': next_token}
        url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/full.json'
        
        
        requests_count += 1
        if requests_count >= 5:
            return df1
        
        response = requests.get(url, headers=header, params=params)
        
        print(response.request.url)
        print("request n.: "+str(requests_count)+" resp code: "+ str(response))
        
        json = response.json()
        df2 = pd.DataFrame(json['results'])
        df1 = pd.concat([df1, df2])
        # next token
        try:
            next_token = json['next']
        except:
            next_token = ' '
            print('no more pages')
    
    return df1

#------------------------------------------ TWEETS COUNT ------------------------------------------

def getTweetsCount(query,lang,fromDate, toDate, lat, long, radius,country):        
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != "-1":
        query = query + ' lang:'+lang
    
    if country != "-1":
        query = query + ' place_country:'+country
        
    # Search using coordinated:  point_radius:[2.355128 48.861118 16km]
    if lat != "-1":
        query = query + " point_radius:["+long+" "+lat+" "+radius+"km]"
        
    # first execution without 'next' param
    params = {'query': query,'fromDate': fromDate, 'toDate': toDate,'bucket':'day' }
    url = "https://api.twitter.com/1.1/tweets/search/fullarchive/full/counts.json"

    response = requests.get(url, headers=header, params=params)
    
    print("Acessando API na URL: "+response.request.url)
    
    # when response code is 429, the requests numbers are exceed
    if response.status_code == 429:
           print("Atenção,Limite de requisições excedido!")
           df1 = pd.DataFrame()
           return df1
               
    print(response)
    
    #gets the response from api
    json = response.json()
    
    #if there's no response, returns an empty dataframe
    try:
        df1 = pd.DataFrame(json['results'])
    except:
        df1 = pd.DataFrame()
        return df1

    # get the next token if exists
    try:
        next_token = json['next']
    except:
        next_token = ' '
        #print('no more pages')

    # loop to get response from the endpoint whith next parameter
    while (next_token != ' '):
    
        params = {'query': query,'fromDate': fromDate, 'toDate': toDate,'bucket':'day', 'next':next_token }
        url = "https://api.twitter.com/1.1/tweets/search/fullarchive/full/counts.json"

        response = requests.get(url, headers=header, params=params)
       
        print("Acessando API na URL: "+response.request.url)
        
        if response.status_code == 429:
           print("Atenção,Limite de requisições excedido!")           
           return df1
       
        print(response)
        json = response.json()
        
        try:
          df2 = pd.DataFrame(json['results'])
        except:
           return df1

        df1 = pd.concat([df1, df2])
        
        # next token
        try:
            next_token = json['next']
        except:
            next_token = ' '
            #print('no more pages')
    
    return df1

#----------------------------------------- RECENT TWEETS COUNT ------------------------------------------

def getTweetsRecentCount(query,lang,fromDate, toDate):        
    
    requests_count = 0     
    
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != "-1":
        query = query + ' lang:'+lang
        
    # first execution without 'next' param
    params = {'query': query, 'granularity':"day",'start_time':fromDate, 'end_time': toDate}
    
    url = 'https://api.twitter.com/2/tweets/counts/recent'

    response = requests.get(url, headers=header, params=params)
    
    print("Acessando API na URL: "+response.request.url)
    
    # when response code is 429, the requests numbers are exceed
    if response.status_code == 429:
           print("Atenção,Limite de requisições excedido!")
           df1 = pd.DataFrame()
           return df1
               
    print(response)
    print(response.request.url)
    #gets the response from api
    json = response.json()
    
    #if there's no response, returns an empty dataframe
    try:
        #df1 = pd.DataFrame(json['results'])
        df1 = pd.DataFrame(json['data'])
    except:
        df1 = pd.DataFrame()
        return df1

    # get the next token if exists
    try:
        next_token = json['next']
    except:
        next_token = ' '
        #print('no more pages')

    # loop to get response from the endpoint whith next parameter
    while (next_token != ' '):
        
        if requests_count == 10:
            return df1
        
        requests_count = requests_count+1
        
        if lang != "-1":
            query = query + ' lang:'+lang
            
        params = {'query': query, 'granularity':"day", 'next':next_token,'start_time':fromDate, 'end_time': toDate }
        url = "https://api.twitter.com/2/tweets/counts/recent"

        response = requests.get(url, headers=header, params=params)
       
        print("Acessando API na URL: "+response.request.url)
        
        if response.status_code == 429:
           print("Atenção,Limite de requisições excedido!")           
           return df1
       
        print(response)
        json = response.json()
        
        try:
          #df2 = pd.DataFrame(json['results'])
          df2 = pd.DataFrame(json['data'])
        except:
           return df1

        df1 = pd.concat([df1, df2])
        
        # next token
        try:
            next_token = json['next']
        except:
            next_token = ' '
            #print('no more pages')
    
    return df1

#-------------------------------------  GET RECENT TWEETS ------------------------------------
def getRecentTweets(query,lang,fromDate, toDate):
    #requests counter:
    requests_count = 0
    
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != '-1':
        query = query + ' lang:'+lang
        
    # first execution without 'next' param
    params = {'query': query, 'max_results': '100', 'start_time':fromDate, 'end_time': toDate,'tweet.fields': 'created_at'}
        
    url = 'https://api.twitter.com/2/tweets/search/recent'            
    
    requests_count += 1
    response = requests.get(url, headers=header, params=params)
    
    
    print(response.request.url)
    print(response.request.body)
    print(response.request.headers)
    print("request n.: "+str(requests_count)+" resp code: "+ str(response))
    
    json = response.json()
    try:
        #df1 = pd.DataFrame(json['results'])
        df1 = pd.DataFrame(json['data'])
    except:
        df1 = pd.DataFrame()
        return df1

    # get the next token if exists
    try:
        #next_token = json['next']
        next_token = json['meta']['next_token']
    except:
        next_token = ' '
        print('no more pages')

    # loop to get response for the endpoint whith next parameter
    while next_token != ' ' :

        params = {'query': query,'next_token': next_token, 'max_results': '100', 'start_time':fromDate, 'end_time': toDate,'tweet.fields': 'created_at'}
        
        url = 'https://api.twitter.com/2/tweets/search/recent'            
        
        requests_count += 1
        # max number of requests
        if requests_count > 100:
            return df1
        
        response = requests.get(url, headers=header, params=params)
        
        print(response.request.url)
        print("request n.: "+str(requests_count)+" resp code: "+ str(response))
        json = response.json()
        #df2 = pd.DataFrame(json['results'])
        df2 = pd.DataFrame(json['data'])
        df1 = pd.concat([df1, df2])
        # next token
        try:
            #next_token = json['next']
            next_token = json['meta']['next_token']
        except:
            next_token = ' '
            print('no more pages')
    
    return df1