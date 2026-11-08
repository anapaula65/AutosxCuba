import requests 
from bs4 import BeautifulSoup 

url = "http://www.cubadebate.cu/" 
headers = {"User-Agent": "Mozilla/5.0"}

respuestas = requests.get(url, headers=headers, timeout=15)
sopa = BeautifulSoup(respuestas.text, "html.parser")

print("Código de respuesta:",
respuestas.status_code)
print("Titulares:")

for titular in sopa.find_all("h2", limit=5):
    print("-", titular.text.strip())
