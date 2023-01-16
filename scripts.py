import requests
import pandas as pd
from io import BytesIO
from datetime import datetime
from flask import Response



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
def formatDates(dt1, dt2):
    
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
    
    return fromDate, toDate

#------------------------------------  GET TWEETS -----------------------------------

def getTweetsFullArchive(query,lang,fromDate, toDate):
    # use the full archive endpoint from twitter api;
    # fromDate and toDate format: '202208250000'
    
    # max number of requests is 10
    requests_count = 0     
    
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != '-1':
        query = query + ' lang:'+lang
        
    # first execution without 'next' param
    params = {'query': query, 'maxResults': '500',
              'fromDate': fromDate, 'toDate': toDate}
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/full.json'
    
    requests_count = requests_count + 1
    
    response = requests.get(url, headers=header, params=params)
    
    print(response.request.url)
    print(response.request.body)
    print(response.request.headers)
    print(response)
    
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
    while next_token != ' ' and requests_count <=3 :
        requests_count = requests_count + 1
        
        params = {'query': query, 'maxResults': '500',
                  'fromDate': fromDate, 'toDate': toDate, 'next': next_token}
        url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/full.json'
        response = requests.get(url, headers=header, params=params)
        print(response)
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

def getTweetsCount(query,lang,fromDate, toDate):        
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != "-1":
        query = query + ' lang:'+lang
        
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

def getTweetsRecentCount(query,lang):        
    
    requests_count = 0     
    
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != "-1":
        query = query + ' lang:'+lang
        
    # first execution without 'next' param
    params = {'query': query, 'granularity':"day"}
    
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
            
        params = {'query': query, 'granularity':"day", 'next':next_token }
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
def getRecentTweets(query,lang):
    #requests counter:
    requests_count = 0
    
    # token from autorization
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA5chgEAAAAA73XpwdJWFyAei9XfNvs%2Fk1vTOws%3DNdKfgnK84FLwadYmIbbGRdr1JeW1aOtJSbCEUi9Rly85VqeM1w"
    header = {"Authorization": 'bearer ' + bearer_token}

    if lang != '-1':
        query = query + ' lang:'+lang
        
    # first execution without 'next' param
    params = {'query': query, 'max_results': '100'}
        
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

        params = {'query': query,'next_token': next_token, 'max_results': '100'}
        
        url = 'https://api.twitter.com/2/tweets/search/recent'            
        
        requests_count += 1
        
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