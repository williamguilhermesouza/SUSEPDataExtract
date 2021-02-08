import requests
from bs4 import BeautifulSoup
import queue
import threading
import json
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

# dumping process numbers to a json
with open('process_numbers.json', 'w') as output:
    output.write(json.dumps(process_numbers))

# creating lists of errors, output, queue and threads
process_errors = []
outputJSON = []
numbers_queue = queue.Queue(-1)
threads = []
queueLock = threading.Lock()
exit_flag = 0


# putting the process numbers to queue
queueLock.acquire()
for number in process_numbers:
    numbers_queue.put(number)
queueLock.release()

# outputting feedback of total process numbers
print(f'Process total: {numbers_queue.qsize()}')

# creating threads using pdf downloader class
for i in range(10):
    threads.append(PdfDownloader(numbers_queue, exit_flag, process_errors, queueLock, outputJSON))
    threads[i].start()

# holding main thread until queue is empty
while not numbers_queue.empty():
    pass

# when queue is empty flagging to threads that they can exit
exit_flag = 1

# joining all threads so they can exit
for t in threads:
    t.join()

# outputting results to json
with open('output.json', 'w') as output:
    output.write(json.dumps(outputJSON))

# outputting errors to json
with open('errors.json', 'w') as output:
    output.write(json.dumps(process_errors))


