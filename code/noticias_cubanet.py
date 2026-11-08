import requests
from bs4 import BeautifulSoup 
url = "https://www.cubanet.org/" 
headers = {"User Agent": "Mozilla/5.0 (x11; Linux x86_64)"} 
respuestas =requests.get(url,headers=headers) 
sopa = BeautifulSoup(respuestas.text, "html.parser")
print("Código de respuesta:", respuestas.status_code)
print("---Títulos de la página:---", sopa.title.text)
for titular in sopa.find_all("h3", limit=5):
    print("-", titular.text.strip())
