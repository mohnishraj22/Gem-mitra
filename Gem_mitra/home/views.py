from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from home import urls
# Create your views here.
def index(request):
    
    return render(request,'index.html')
def geturl(request):
    main_url=request.GET['url']
    print(main_url)
    def get_title(soup):
        try:
            title = soup.find('h1',attrs={'class' : "like-h3",'itemprop' : "name" }).text.replace('\n','').replace('         ','')
            title_string = title.strip()
        except AttributeError:
            title_string = ""
        return title_string

    def get_price(soup):
        try:
            price = soup.find('span',attrs={'class' : "m-w"}).text
        except AttributeError:
                price = ""
        return price


    def get_rating(soup):
        try:
            rating = soup.find('span',attrs={'class' : "badge"}).text
        except AttributeError:
                rating = ""
        return rating
    def get_availability(soup):
        try:
            availability = soup.find('strong',attrs={'class' : "green"}).text.replace('\n', '').replace('      ', ' ')
        except AttributeError:
            availability = "Not Available"
        return availability
    
    def get_data(url):
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, "html.parser")
        d = {"title":[], "price":[], "rating":[],"availability":[]}

        d['title'].append(get_title(soup))
        d['price'].append(get_price(soup))
        d['rating'].append(get_rating(soup))
        d['availability'].append(get_availability(soup))
        
        return d
    temp=get_data(main_url)
    gem_def=pd.DataFrame.from_dict(temp)
    data={'title':temp['title'][0],'price':temp['price'][0],'rating':temp['rating'][0],'url':main_url}
    print(temp)
    def api_data(gem_df):
        name = gem_df['title']

        url = "https://real-time-amazon-data.p.rapidapi.com/search"

        querystring = {"query":name,"page":"1","country":"IN","category_id":"aps"}

        headers = {
            "X-RapidAPI-Key": "f39e332248msh4b2bab8450682cfp1b705cjsne97a09c6b7a7",
            "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
        }


        response = requests.get(url, headers=headers, params=querystring)
        df = pd.DataFrame(response.json()['data']['products'])
        
        return df

        
    temp1=api_data(temp)
    print(temp1)
    def compare(data,var):
        df=data
        df.fillna(0,inplace=True)
        df['product_price'] = df['product_price'].replace('[\₹\,\.]', '', regex=True).astype(int)
        df["price_norm"] = MinMaxScaler().fit_transform(np.array(df['product_price']).reshape(-1,1))
        df["rating_norm"] = MinMaxScaler().fit_transform(np.array(df['product_star_rating']).reshape(-1,1))
        df['comparing_col']=-0.7*df['price_norm']+0.3*df['rating_norm']
        df.sort_values(by=['comparing_col'],axis=0, ascending=False, inplace=True)
        
        new_df=df.head(var)
        index = pd.Index(range(0,var,1))
        new_df = new_df.set_index(index)
        return new_df
    comp=compare(temp1,1)
    print(comp)
    dict1=comp.to_dict()
    print(dict1)
    data_api={'product_title':dict1['product_title'][0],'product_price':dict1['product_price'][0],'product_star_rating':dict1['product_star_rating'][0],'product_photo':dict1['product_photo'][0],'product_url':dict1['product_url'][0]}
    
    def range_to_average(text):
        val1 , val2 = text.split('-')
        val1=float(val1)
        val2=float(val2)
        avg=(val1+val2)/2
        return avg

    def Remove_Currency(input_string):

        input_string=input_string.replace("Rs.","")
        input_string=input_string.replace(",","")
        return (input_string)
    
    def FinalCompare(file1,file2):
        file1.drop(['price_norm', 'rating_norm','comparing_col'], axis=1)
        file2['rating']=file2['rating'].apply(range_to_average)
        file2['price'] = file2['price'].apply(Remove_Currency).astype(float)
        final_df = pd.concat([file1,file2])
        final_df["price_norm"] = MinMaxScaler().fit_transform(np.array(final_df['price']).reshape(-1,1))
        final_df["rating_norm"] = MinMaxScaler().fit_transform(np.array(final_df['rating']).reshape(-1,1))
        final_df['comparing_col']=-0.7*final_df['price_norm']+0.3*final_df['rating_norm']
        final_df.sort_values(by=['comparing_col'],axis=0, ascending=False, inplace=True)
        final_df=final_df.head(1)
        return final_df
            
    try:
        comp1=compare(temp1,2)
        dict2=comp1.to_dict()
        data_api1={'product_title':dict2['product_title'][1],'product_price':dict2['product_price'][1],'product_star_rating':dict2['product_star_rating'][1],'product_photo':dict2['product_photo'][1],'product_url':dict2['product_url'][1]}
        # best=FinalCompare(gem_def,comp1)
        # print(best)
        dict={'gem_data':data,'fetch_data':data_api,'fetch_data1':data_api1}  
    except:
        # best=FinalCompare(gem_def,comp)
        # print(best)
        dict={'gem_data':data,'fetch_data':data_api}
        
    
    return render(request,'url.html' ,context=dict)

# dict['product_title'][1] ? {'product_title':dict1['product_title'][0],'product_price':dict1['product_price'][0],'product_star_rating':dict1['product_star_rating'][11],'product_photo':dict1['product_photo'][0],'product_url':dict1['product_url'][0]}
    
def about(request):
    return render(request,'about.html') 

def contact(request):
    return render(request,'contact.html') 

def login(request):
    return render(request,'login.html') 

def help(request):
    return render(request,'help.html') 