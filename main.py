import requests
from bs4 import BeautifulSoup

# getting the data from susep
raw_data = requests.get('http://dados.susep.gov.br/olinda-ide/servico/produtos/versao/v1/odata/DadosProdutos?$format=json')

# saving the raw data locally
with open('raw_data', 'w') as output:
    output.write(raw_data.text)

# parsing raw data to dictonary format
json_data = raw_data.json()

# filtering the data by tipoproduto
filtered_data = [product for product in json_data['value'] if product['tipoproduto'] == 'PLANO DE PREVIDÊNCIA']

# filtering the data for process numbers
process_numbers = [number['numeroprocesso'] for number in filtered_data]

for number in process_numbers:
    susep_page = requests.post('https://www2.susep.gov.br/safe/menumercado/REP2/Produto.aspx/Consultar', { 'numeroProcesso' : number })
    
    soup = BeautifulSoup(susep_page.text, 'html.parser')

    pdf_link = f'https://www2.susep.gov.br{soup.a["onclick"][15:-1]}'

    pdf = requests.get(pdf_link)

    with open(number, 'wb') as output:
        output.write(pdf.content)


