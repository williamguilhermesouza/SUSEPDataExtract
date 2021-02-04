from threading import Thread
import requests
from bs4 import BeautifulSoup

class PdfDownloader(Thread):
    def __init__(self, queue, exit_flag, process_errors):
        Thread.__init__(self)
        self.queue = queue
        self.exit_flag = exit_flag
        self.process_errors = process_errors

    def run(self):
        while not self.exit_flag:
            if not self.queue.empty():
                number = self.queue.get()
                if self.queue.qsize() % 10 == 0:
                    print(f'Remaining: {self.queue.qsize()}')

            try:
                susep_page = requests.post('https://www2.susep.gov.br/safe/menumercado/REP2/Produto.aspx/Consultar', { 'numeroProcesso' : number })
            except:
                error = f'Query error in process {number}'
                print(error)
                self.process_errors.append({number: error})
                continue

            soup = BeautifulSoup(susep_page.text, 'html.parser')

            try:
                pdf_link = f'https://www2.susep.gov.br{soup.a["onclick"][15:-1]}'
                
                pdf_name = f'{str(number).replace("/", "-")}.pdf'
            except:
                error = f'PDF Link construction error in process {number}'
                print(error)
                self.process_errors.append({number: error})
                continue


            try:
                pdf = requests.get(pdf_link)
            except:
                error = f'PDF error in process {number}'
                print(error)
                self.process_errors.append({number: error})
                continue

            with open(pdf_name, 'wb') as output:
                output.write(pdf.content)
