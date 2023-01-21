import requests
import lxml.html as html
import os 
import datetime


HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//div[@class="V_Title"]/a/@href'
XPATH_TITLE = '//div[1]/h2/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link,today):
	
	try:
		response = requests.get(link)
		if response.status_code == 200:
			notice = response.content.decode('utf-8')
			parsed = html.fromstring(notice)
			
			try:
				title = parsed.xpath(XPATH_TITLE)[0]
				title = title.replace('\"','')
				title = title.replace('\"','')
				title = title.replace('#','')
				title = title.replace('|','')			
				print(title)		
				summary = parsed.xpath(XPATH_SUMMARY)[0]
				#print(f'Este es el resumen : {summary}')
				body = parsed.xpath(XPATH_BODY)
				#print(f'este es el cuerpo : {body}')
				
			except IndexError:
				return 
			
			with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
				f.write(title)
				f.write('\n\n')
				f.write(summary)
				f.write('\n\n')
				for p in body:
					f.write(p)
					f.write('\n')
				
				print('Se creo archivo')
		else:
			raise ValueError(f'Error: {response.status_code}')
	except ValueError as ve:
		print(ve)



def parse_home():
	try:
		response = requests.get(HOME_URL)
		if response.status_code == 200:
			home = response.content.decode('utf-8')
			parsed = html.fromstring(home)
			links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
			print(links_to_notices)
			
			today = datetime.date.today().strftime('%d-%m-%y')
			if not os.path.isdir(today):
				os.mkdir(today)
			
			for link in links_to_notices:
				parse_notice(link,today)
				#print(link)
		else:
			raise ValueError(f'Error:{response.status_code}')	
	except ValueError as ve:
		print(ve)

def run():
	parse_home()

if __name__ == '__main__':
	run()









