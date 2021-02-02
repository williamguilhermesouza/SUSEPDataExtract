import requests

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

print(process_numbers)