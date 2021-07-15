from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from requests.auth import HTTPDigestAuth
from lxml import html
import json
import re
import codecs
from os import walk


def scrapeCRhtml(product):
	HtmlFile = open("/Users/djolear/Google Drive/research/projects/emcr/cr_data/cr_html/" + product + ".html", 'r', encoding='utf-8')
	source_code = HtmlFile.read()
	soup = BeautifulSoup(source_code, features = "lxml")
	titles = soup.findAll('div', attrs = {'class': 'crux-component-title list__model'})
	scores = soup.findAll('div', attrs = {'class': 'ratings-overall-score'})
	prices = soup.findAll('div', attrs = {'class': 'list__price'})
	
	df_titles = pd.DataFrame(columns=['Name'])
	df_prices = pd.DataFrame(columns=['cr_price'])
	for i in range(len(titles)):
		d = {'Name': [titles[i].text.strip()]}
		df = pd.DataFrame(data=d)
		df_titles = df_titles.append(df)

		d = {'cr_price': [prices[i].text.strip().replace('Price', '').replace(' ', '')]}
		df = pd.DataFrame(data=d)
		df_prices = df_prices.append(df)


	df_scores = pd.DataFrame(columns=['overall_score'])
	for i in range(0, len(scores), 2):
		d = {'overall_score': [scores[i].text.strip()]}
		df = pd.DataFrame(data=d)
		df_scores = df_scores.append(df)

	df_main = pd.concat([df_titles.reset_index(drop=True), df_scores.reset_index(drop=True)], axis=1)
	df_main = pd.concat([df_main.reset_index(drop=True), df_prices.reset_index(drop=True)], axis=1)
	
	labels = soup.findAll('div', attrs = {'class': 'crux-ratings-attribute-bar__label'})
	subscores = soup.findAll('div', attrs = {'class': 'crux-ratings-attribute-bar__bar'})

	df_subscores = pd.DataFrame(columns=['index', 'label', 'subscore'])
	ind = 0
	j = 0
	for i in range(len(labels)):
		d = {'index': [ind], 'label': [labels[i].text.strip()], 'subscore': [subscores[i].text.strip()]}
		df = pd.DataFrame(data=d)
		df_subscores = df_subscores.append(df)
		if j == (len(subscores) / len(titles) - 1):
			j = 0
			ind += 1
		else:
			j += 1

	df_subscores = df_subscores.pivot(index = 'index', columns='label', values='subscore')
	df_main = pd.concat([df_main.reset_index(drop=True), df_subscores.reset_index(drop=True)], axis=1)

	df_main.to_csv("/Users/djolear/Google Drive/research/projects/emcr/cr_data/cr_scraped/" + product + '_cr.csv')



mypath = "/Users/djolear/Google Drive/research/projects/emcr/cr_data/cr_html/"

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
	f.extend(filenames)
	break

filenames = pd.DataFrame(data = f, columns = ['filename'])

filenames = filenames[filenames['filename'].str.contains(".html")]

filenames['filename'] = filenames['filename'].str.replace('.html','')

for i, j in filenames.iterrows(): 
	print("Starting " + filenames.filename[i] + ".")
	scrapeCRhtml(filenames.filename[i])
 


