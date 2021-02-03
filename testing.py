import requests
from bs4 import BeautifulSoup

data = requests.post('https://www2.susep.gov.br/safe/menumercado/REP2/Produto.aspx/Consultar', { 'numeroProcesso' : '15414.607577/2020-12'})


soup = BeautifulSoup(data.text, 'html.parser')

pdf_link = f'https://www2.susep.gov.br{soup.a["onclick"][15:-1]}'

print(pdf_link)

pdf = requests.get(pdf_link)

with open('pdf', 'wb') as out:
    out.write(pdf.content)


