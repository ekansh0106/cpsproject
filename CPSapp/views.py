from django.shortcuts import render
import numpy as np
import pandas as pd
import csv
from . import twitter as t

global search


def home(request):
    return render(request,'CPSapp/homepage.html')

def about (request):
    return render(request,'CPSapp/aboutme.html')

def search(mycity):
    datasetHotel = pd.read_csv('F:\\BE-proj-master\\updated python files\\hotelDataset.csv')
    #datasetHotel.drop(["Unnamed: 4","Unnamed: 5","Unnamed: 6","Unnamed: 7","Unnamed: 8","Unnamed: 9","Unnamed: 10","Unnamed: 11","Unnamed: 12","Unnamed: 13","Unnamed: 14","Unnamed: 15","Unnamed: 16","Unnamed: 17","Unnamed: 18","Unnamed: 19","Unnamed: 20","Unnamed: 21","Unnamed: 22","Unnamed: 23","Unnamed: 24","Unnamed: 25","Unnamed: 26"], axis = 1, inplace = True) 
    datasetHotel.drop(["property_id", "property_name","state"], axis = 1, inplace = True)
    #datasetHotel.drop(["tad_stay_review_rating"], axis = 1, inplace = True)
    #datasetHotel.drop(["property_id"], axis = 1, inplace = True)
    datasetHotel = datasetHotel.drop(datasetHotel.index[[11267]])
    datasetHotel["site_review_rating"] = pd.to_numeric(datasetHotel["site_review_rating"])
    newDatasetHotel = datasetHotel[np.isfinite(datasetHotel['site_review_rating'])]
    #x=input("Enter the City Name")
    
    print (newDatasetHotel[newDatasetHotel["city"] == mycity])
    a = newDatasetHotel[newDatasetHotel["city"] == mycity]
    print("Average rating in %s is" %mycity)
    result = np.mean(a.iloc[:, 2].values)
    return result

def predict (mycity,myweek):
    import matplotlib.pyplot as plt

    from pytrends.request import TrendReq
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [mycity]
    pytrends.build_payload(kw_list, cat=0, timeframe='2016-01-06 2018-12-31', geo='', gprop='')
    
    dataset = pytrends.interest_over_time()
    #print (dataset)
    
    Y = dataset.iloc[:, :-1].values
    #print (Y)
    #len (Y)
    
    A =  [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
    
    X = np.asarray(A)
    
    #print (X)
    #len (X)
    
    def chunks(l, n):
  
        for i in range(0, len(l), n):
        
            yield l[i:i+n]
            
    E=list(chunks(Y, 52))

    newDataset = []
    
    L = E[0]
    M = E[1]
    N = E[2]
    #O = E[3]
    #P = E[4] 
    
    for i in range(0,52):
        newDataset.append((np.mean(L[i])+ np.mean(M[i])+np.mean(N[i]))/3) 
    
    #len(newDataset)
    finalDataset = np.reshape(newDataset, (-1,1))
    X = np.reshape(X,(-1,1))

    #print(finalDataset)
    #len (finalDataset)
    #len (X)
        
    from sklearn.linear_model import LinearRegression
    lin_reg = LinearRegression()
    lin_reg.fit(X, finalDataset)
    
    # Fitting Polynomial Regression to the dataset
    from sklearn.preprocessing import PolynomialFeatures
    poly_reg = PolynomialFeatures(degree = 9)
    X_poly = poly_reg.fit_transform(X)
    poly_reg.fit(X_poly, finalDataset)
    lin_reg_2 = LinearRegression()
    lin_reg_2.fit(X_poly, finalDataset)

    """# Visualising the Linear Regression results
    #plt.scatter(X, Y, color = 'red')
    #plt.plot(X, lin_reg.predict(X), color = 'blue')
    #plt.title('Truth or Bluff (Linear Regression)')
    #plt.xlabel('Interest')
    plt.ylabel('Week')
    plt.show()"""
    
    X_grid = np.arange(min(X), max(X), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    plt.scatter(X, finalDataset, color = 'red')
    plt.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')
    plt.grid()
    plt.title('Weekly Interest at ' + mycity )
    plt.xlabel('Week Number')
    plt.ylabel('Interest')
    plt.show()
    
    
    t = lin_reg_2.predict(poly_reg.fit_transform([[myweek]]))
    t = t.astype(np.float64)
    s = finalDataset[[int(myweek)]]
    p = str(t[0]).replace('[','').replace(']','')
    s = str(s[0]).replace('[','').replace(']','')
    #p = " ".join(p)
    return p,s
     

def tweets (mycity):
    # creating object of TwitterClient Class 
    api = t.TwitterClient() 
	# calling function to get tweets 
    tour = " trip"
    tweets = api.get_tweets(query = mycity + tour, count = 200) 

	# picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# percentage of positive tweets 
    ptp = 100*len(ptweets)/len(tweets)
	# picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    ntp = 100*len(ntweets)/len(tweets)
	# printing first 5 positive tweets  
    
    pt = []
    for tweet in ptweets[:20]:
        pt.append(tweet['text']) 

    # printing first 5 negative tweets 
    nt = []
    for tweet in ntweets[:10]: 
    	nt.append(tweet['text']) 
    return ptp,ntp,pt,nt




def disp (request):
    myweek = request.POST[ 'week' ]
    mycity = request.POST[ 'city' ]
    avrg = search(mycity)
    pre = []
    pre = predict(mycity,myweek)
    p = pre[0]
    s = pre[1]
    twt = []
    twt = tweets(mycity)
    ptp = twt[0]
    ntp = twt[1]
    pt = twt[2]
    nt = twt[3]
    return render(request,'CPSapp/page2.html',{'myweek': myweek ,'mycity': mycity,'avrg': avrg,'p':p,'s':s,'ptp': ptp,'ntp':ntp,'pt':pt,'nt':nt,})
