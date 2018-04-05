#import libs
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pyrebase

config = {
  "apiKey": "AIzaSyBDTC-8AlaANFtKO5AglxGCglLKJ2bxAQI",
  "authDomain": "praga-app.firebaseapp.com",
  "databaseURL": "https://praga-app.firebaseio.com",
  "storageBucket": "praga-app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


with open('links-formigas.txt') as f:
	links = f.readlines()

links = [x.strip() for x in links]

for link in links:
	page = urlopen(link)
	soup = BeautifulSoup(page, 'html.parser')

	nome = soup.find('h1', attrs={'class', 'bottommargin cor-agricultura'})
	nome = nome.text.strip()

	nomeCientifico = ""
	
	h4 = soup.find_all('h4', attrs={'class', 'cor-agricultura'})
	for value in h4:
		nomeCientifico = value.find('b')
		if nomeCientifico != None:
			soup_i = BeautifulSoup(nomeCientifico)
			final = soup_i.find('i')
			print(final)


#nome:nome,
#nomeCientifico:cientifico,
#link:link,
#culturasAfetadas:culturas,
#danos:danos,
#descricao:desc,
#controle:ctrl,
#tipo:tipo