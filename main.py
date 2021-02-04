import requests
from bs4 import BeautifulSoup
import queue
import threading
from PdfProcessing import PdfDownloader

# getting the data from susep
try:
    raw_data = requests.get('http://dados.susep.gov.br/olinda-ide/servico/produtos/versao/v1/odata/DadosProdutos?$format=json')
except:
    raise('Raw data query error')

# saving the raw data locally
with open('raw_data.json', 'w') as output:
    output.write(raw_data.text)

# parsing raw data to dictonary format
json_data = raw_data.json()

# filtering the data by tipoproduto
filtered_data = [product for product in json_data['value'] if product['tipoproduto'] == 'PLANO DE PREVIDÊNCIA']

# filtering the data for process numbers
process_numbers = [number['numeroprocesso'] for number in filtered_data]

with open('process_numbers.json', 'w') as output:
    output.write(str(process_numbers))

process_errors = []
numbers_queue = queue.Queue(-1)
threads = []
queueLock = threading.Lock()
exit_flag = 0


queueLock.acquire()
for number in process_numbers:
    numbers_queue.put(number)
queueLock.release()


print(f'Total de processos: {numbers_queue.qsize()}')

for i in range(10):
    threads.append(PdfDownloader(numbers_queue, exit_flag, process_errors, queueLock))
    threads[i].start()

while not numbers_queue.empty():
    pass

exit_flag = 1

for t in threads:
    t.join()

with open('errors', 'w') as output:
    output.write(str(process_errors))



'''
    try:
        susep_page = requests.post('https://www2.susep.gov.br/safe/menumercado/REP2/Produto.aspx/Consultar', { 'numeroProcesso' : number })
    except:
        error = f'Query error in process {number}'
        print(error)
        process_errors.append({number: error})
        continue

    soup = BeautifulSoup(susep_page.text, 'html.parser')

    try:
        pdf_link = f'https://www2.susep.gov.br{soup.a["onclick"][15:-1]}'
        
        pdf_name = f'{str(number).replace("/", "-")}.pdf'
    except:
        error = f'PDF Link construction error in process {number}'
        print(error)
        process_errors.append({number: error})
        continue


    try:
        pdf = requests.get(pdf_link)
    except:
        error = f'PDF error in process {number}'
        print(error)
        process_errors.append({number: error})
        continue

    with open(pdf_name, 'wb') as output:
        output.write(pdf.content)

'''
