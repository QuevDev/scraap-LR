#!/usr/bin/env python
# coding: utf-8

import requests 
from bs4 import BeautifulSoup


URL = 'https://www.pagina12.com.ar/'

#para generar una solicitud usamos el modulo requests

pagina = BeautifulSoup(requests.get(URL).text,'lxml')

def get_links(soup):
  
    s = soup.find_all('div',attrs={'class':'article-title'})
        
    links=[]
        
    for tag in s:
        link = tag.a['href']
        links.append(link)
    print(links) 
  

def run(pagina):
	get_links(pagina)

if __name__ == '__main__':
	run(pagina)







