from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import urllib3
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

def searchAsin(asin):
	url = "https://www.amazon.com/dp/" + asin
	page = requests.get(url, proxies = proxies, verify = False)
	if page.status_code == 200:
		return page
	else:
		return "Error"

def searchReviews(url):
	page = requests.get(url, proxies = proxies, verify = False)
	if page.status_code==200:
		return page
	else:
		return "Error"


def url_link(query):
	url="https://www.amazon.com/dp/" + str(query)     #search link
	page = requests.get(url, proxies = proxies, verify = False)
	if page.status_code==200:
		return page                            #return the page if there is no error
	else:
		return "Error"


def get_amazon_review_links(product):

	asins = pd.read_csv(my_path + "research/projects/emcr/emcr_amzcr_data/asins_checked_cleaned/" + product + "_asins_checked_cleaned.csv")

	links = []

	for i in range(asins['asin_number'].count()):
		links.append("https://www.amazon.com/dp/" + str(asins.asin_number[i]))

	reviewLinks = pd.DataFrame() 
	num_complete = 0

	for i in range(len(asins['asin_number'])):
		if pd.isna(asins.asin_number[i]) == False:
			attempts = 0
			while attempts < 5:
				try:
					link_response = url_link(asins.asin_number[i])

					#iterates through Asin no to access the product
					soup = BeautifulSoup(link_response.content, features = "lxml")

					j = 0
					for i in soup.findAll('a',attrs={'data-hook':'see-all-reviews-link-foot'}):
						if (j > 0): break
						reviewLinks = reviewLinks.append([i['href']])    
						j = j + 1
					break

				except Exception:
					attempts += 1
					print(asins.asin_number[i] + ' trying again')
					time.sleep(5)
					

		elif pd.isna(asins.asin_number[i]) == True:
			reviewLinks = reviewLinks.append(["NA"])

		num_complete += 1    
		num_remaining = asins.asin_number.count() - num_complete
		print(str(num_complete) + " " + product + "(s) complete. " + str(num_remaining) + " products remaining.")
		time.sleep(5)

	products = pd.DataFrame(columns=['asin'])
	products['asin'] = asins.asin_number

	reviewLinks = reviewLinks.rename(columns={0: "link"})
	reviewLinks = reviewLinks.reset_index()
	reviewLinks = reviewLinks['link']

	products['link'] = reviewLinks

	print(products)

	products.to_csv(my_path + "research/projects/emcr/emcr_amzcr_data/review_links/" + product + "_review_links.csv")


#get_amazon_review_links("coffee_makers_drip")

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
    get_amazon_review_links(filenames.filename[i])