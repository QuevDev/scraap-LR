import requests
import lxml.html as html
import os 
import datetime

name_p = 'hyperx'

HOME_URL = f'https://www.spdigital.cl/categories/search?q={name_p}&category_id=-1'
BASE_URL = 'https://www.spdigital.cl'
XPATH_HREF = '//div[@class="name"]/a/@href'
XPATH_TITLE = '//div[@class="span7"]/h1/text()'
XPATH_VALUE ='//span[@class="product-view-cash-price-value text-webstore"]/text()'
XPATH_BRAND = '//span[@itemprop="name"]/text()'
XPATH_CODE = '//span[@itemprop="sku"]/text()'

def parse_product(link, today):
	try:
		response = requests.get(link)
		if response.status_code == 200:
			product = response.content.decode('utf-8')
			parsed = html.fromstring(product)
			
			try:
				title  = parsed.xpath(XPATH_TITLE)[0]
				title = title.replace(' ','')
				print(title)
				brand = parsed.xpath(XPATH_BRAND)[0]
				print(brand)
			    #elimino los espacios en los precios
				precios = parsed.xpath(XPATH_VALUE)
				precios = [precios[i].replace(' ','').replace('\r','').replace(' \n','') for i in range(len(precios))]
				normal_value = precios[0]
				efective_value = precios[1]
				print(normal_value,efective_value)
				
				
				code = parsed.xpath(XPATH_CODE)[0]	
				document_name = brand+code	
				document_name = document_name.replace('/','')		

			except IndexError as e:
				print(e)
		
			with open(f'{today}/{document_name}.txt','w',encoding='utf-8') as f:
				f.write(title)
				f.write('\n')
				f.write(f'marca : {brand}')
				f.write('\n')				
				f.write(f'Precio normal : {normal_value}')
				f.write('\n')
				f.write(f'Precio Efectivo : {efective_value}')
				f.write('\n')
				
		else:
			raise ValueError(f'error : {repsonse.status_code}')
	except ValueError as ve:
		print(ve)

def parse_home():
	try:
		response = requests.get(HOME_URL)
		if response.status_code ==200:
			home = response.content.decode('utf-8')
			parsed = html.fromstring(home)
			links_to_products = parsed.xpath(XPATH_HREF)
			
			today = datetime.date.today().strftime('%d-%m-%y')
			if not os.path.isdir(today):
				os.mkdir(today)
			

			l = len(links_to_products)
			for i in range(l):
				links_to_products[i] = BASE_URL+links_to_products[i]
			print(links_to_products)
			
			for link in links_to_products:
				parse_product(link,today)	
			
			
				

	except ValueError as ve:
		print('error',ve)

def run():
	parse_home()

if __name__ == '__main__':
	run()





