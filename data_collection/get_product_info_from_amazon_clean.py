import pandas as pd
import numpy as np
import time
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from difflib import SequenceMatcher
import urllib3
import re
import time
from os import walk

# Set path
import platform
my_system = platform.uname()

if(my_system.node == "asdf1234"):
    my_path = "G:/My Drive/"
else:
    my_path = "/Users/djolear/Google Drive/"


urllib3.disable_warnings()

proxy_host = "proxy.crawlera.com"
proxy_port = "8013"
proxy_auth = "a76c96b9f8ae43a18d07ff5c38c398f2:" # Make sure to include ':' at the end
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
      "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}


# Function to extract Product Title
def get_title(soup):
     
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
 
        # Inner NavigableString Object
        title_value = title.string
 
        # Title as a string value
        title_string = title_value.strip()
 
        # # Printing types of values for efficient understanding
        # print(type(title))
        # print(type(title_value))
        # print(type(title_string))
        # print()
 
    except AttributeError:
        title_string = ""   
 
    return title_string
 
# Function to extract Product Price
def get_price(soup):
 
    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
 
    except AttributeError:
        price = ""  
 
    return price
 
# Function to extract Product Rating
def get_rating(soup):
 
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
         
    except AttributeError:
         
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = "" 
 
    return rating
 
# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
         
    except AttributeError:
        review_count = ""   
 
    return review_count
 
# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
 
    except AttributeError:
        available = ""  
 
    return available

def get_model_number(soup):
    try:
        product_details = soup.find(attrs={'class':'a-keyvalue prodDetTable'})
        product_details = product_details.findAll(attrs={'class':'a-size-base'})
        if len(product_details) > 10:
            model_number = product_details[9].string.strip()
        else:
            model_number = ""  


    except AttributeError:
        model_number = ""  
 
    return model_number


def getProductInfo(asin):
    url="https://www.amazon.com/dp/" + str(asin)
    # print(url)
    page = requests.get(url, proxies=proxies, verify=False)

    soup = BeautifulSoup(page.content, features = "lxml")
    
    amazon_title = []
    price = []
    avgRating = []
    reviewCount = []
    model_number = []
    amazon_title.append(get_title(soup))
    
    price = get_price(soup)
    avgRating = get_rating(soup)
    reviewCount = get_review_count(soup)
    df = pd.DataFrame(columns=['title'])
    model_number = get_model_number(soup)
    
    df['amazon_title'] = amazon_title
    df['amazon_price'] = np.array(price)
    df['avgRating'] = np.array(avgRating)
    df['reviewCount'] = np.array(reviewCount)
    df['model_number'] = np.array(model_number)
    
    return df

def substringFinder(string1, string2):
    answer = ""
    anslist=[]
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                #if (len(match) > len(answer)): 
                answer = match
                if answer != '' and len(answer) > 1:
                    anslist.append(answer)
                match = ""

        if match != '':
            anslist.append(match)
        # break
    return anslist

def getProductInfoMaster(product):
    df = pd.read_csv(my_path + "research/projects/emcr/emcr_amzcr_data/asins_checked_cleaned/" + product + '_asins_checked_cleaned.csv')
    dfProductInfo = pd.DataFrame() 
    print("Starting " + product + ".")
    for i in range(len(df.asin_number)):
        if pd.isna(df.asin_number[i]) == True:
            dfNA = pd.DataFrame(data = np.array([["NA", "NA", "NA", "NA", "NA"]]),columns=['amazon_title', 'amazon_price', 'avgRating', 'reviewCount', 'model_number'])
            dfProductInfo = dfProductInfo.append(dfNA)
        elif pd.isna(df.asin_number[i]) == False:
            dfProductInfo = dfProductInfo.append(getProductInfo(df.asin_number[i]))
        time.sleep(4)
        num_complete = i + 1    
        num_remaining = len(df.asin_number) - i
        print(str(num_complete) + " " + product + "(s) complete. " + str(num_remaining) + " products remaining.")

    df = pd.concat([df.reset_index(drop=True), dfProductInfo.reset_index(drop=True)], axis=1)

    for i in range(df['Name'].count()):
        df.avgRating[i] = df.avgRating[i].replace('out of 5 stars', '')
        df.reviewCount[i] = df.reviewCount[i].replace('ratings', '')
        df.reviewCount[i] = df.reviewCount[i].replace(',', '')
        df.Name[i] = df.Name[i].lower()
        df.amazon_title[i] = df.amazon_title[i].lower()
        df.model_number[i] = df.model_number[i].lower()

    df = df[['Name', 'amazon_title', 'model_number', 'asin_number', 'amazon_price', 'avgRating', 'reviewCount']]

    df.to_csv(my_path + "research/projects/emcr/emcr_amzcr_data/amazon_product_info_second_pass/" + product + "_wpi.csv")


#getProductInfoMaster("coffee_makers_drip")

#/Users/djolear/Google Drive/
#G:/My Drive

# Run functions
data_path = my_path + "research/projects/emcr/emcr_amzcr_data/asins_checked_cleaned/"


f = []
for (dirpath, dirnames, filenames) in walk(data_path):
    f.extend(filenames)
    break

filenames = pd.DataFrame(data = f, columns = ['filename'])

filenames = filenames[filenames['filename'].str.contains("_asins_checked_cleaned.csv")]

filenames['filename'] = filenames['filename'].str.replace('_asins_checked_cleaned.csv','')

for i, j in filenames.iterrows(): 
    getProductInfoMaster(filenames.filename[i])
