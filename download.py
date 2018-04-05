#import libs
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pyrebase
import re
import time

config = {
  "apiKey": "AIzaSyBDTC-8AlaANFtKO5AglxGCglLKJ2bxAQI",
  "authDomain": "praga-app.firebaseapp.com",
  "databaseURL": "https://praga-app.firebaseio.com",
  "storageBucket": "praga-app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


with open('links-plantas-invasoras.txt') as f:
	links = f.readlines()

links = [x.strip() for x in links]

for link in links:
	page = urlopen(link)
	soup = BeautifulSoup(page, 'html.parser')


	# Encontrar nome
	nome = soup.find('h1', attrs={'class', 'bottommargin cor-agricultura'})
	nome = nome.text.strip()	

	# Encontrar nome científico

	nomeCientifico = ""
	h4 = soup.find_all('h4', attrs={'class', 'cor-agricultura'})
	for value in h4:
		s = value.find('b')
		if s != None:
			s = s.text.strip()
			s = s[s.find("(")+1:s.find(")")]
			nomeCientifico = s
			break

	#print(s)

	# Encontrar culturas afetadas
	p = soup.p.text
	culturasAfetadas = p[19:]
	#print(p)

	# Encontrar Link
	link_praga = link
	#print(link)

	# Encontrar descricao
	allP = soup.find_all('p', {'style' : 'text-align: justify'})
	texto = ""
	for item in allP:
		texto += item.text.strip()

	descricao = ""

	m = re.search("googletag.cmd", texto)
	if m != None:
		descricao = texto[:m.start() - 4]
	#print(descricao)

	# Encontrar danos

	danos = ""

	inicio = re.search("Danos: ", texto)
	fim = re.search("Controle:", texto)
	if inicio != None and fim != None:
		danos = texto[inicio.start()+7:fim.start()]
		#print(danos + "\n\n")

	#

	controle = ""

	if fim != None:
		controle = texto[fim.start()+10:]
		#print(controle + "\n\n")

	tipo = "Plantas Invasoras"

	uid = nomeCientifico.replace(" ", "_")
	uid = uid.replace(".", "")
	uid = uid.replace("-", "_")
	uid = uid.replace("\t","")

	print("\n\n")
	print("ID: " + uid)
	print("NOME: " + nome)
	print("NOME CIENTIFICO: " + nomeCientifico)
	print("LINK:" + link)
	print("CULTURAS AFETADAS: " + culturasAfetadas)
	print("DANOS: " + danos)
	print("CONTROLE: " + controle)
	print("DESCRICAO: " + descricao)
	print("TIPO: " + tipo)
	print("\n\n")


	dados = {
		"controle":controle,
		"culturasAfetadas":culturasAfetadas,
		"danos":danos,
		"descricao":descricao,
		"link":link,
		"nome":nome,
		"nomeCientifico":nomeCientifico,
		"tipo":tipo
	}
	
	db.child("pragas").child(uid).set(dados)