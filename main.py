import requests

raw_data = requests.get('http://dados.susep.gov.br/olinda-ide/servico/produtos/versao/v1/odata/DadosProdutos?$format=json')

json_data = raw_data.json()

filtered_data = [product for product in json_data if product.tipoproduto == 'PLANO DE PREVIDÊNCIA']

print(filtered_data)
