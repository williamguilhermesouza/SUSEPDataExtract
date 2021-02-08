from threading import Thread
import requests
from bs4 import BeautifulSoup
import PdfExtractor

## This class is a subclass of the Thread class from threading,
# and as so it creates subthreads to share the workload of 
# downloading all the pdfs and processing, so it takes less time.
# Initially, the work for pdf downloading with one thread took
# around 5 hours. After working with 10 threads, without the 
# pdf processing it took around 20 minutes. With all the pdf
# processing and work it took 2 hours.
## The thread runs when called the start method, and it runs 
# the code in the run method.
class PdfDownloader(Thread):
    # Initializing the variables that are passed from the main thread
    def __init__(self, queue, exit_flag, process_errors, queueLock, outputJSON):
        Thread.__init__(self)
        self.queue = queue
        self.exit_flag = exit_flag
        self.process_errors = process_errors
        self.queueLock = queueLock
        self.outputJSON = outputJSON
    # run method that holds all the code
    def run(self):
        # looks for an exit flag controlled by the main thread 
        while not self.exit_flag:
            # acquire the lock to use the queue
            self.queueLock.acquire()
            # looks if the queue is empty to stop the work
            if not self.queue.empty():
                # taking a number from the queue and releasing the lock so it can be used by another thread
                number = self.queue.get()
                self.queueLock.release()
                # printing feedback of the downloads from 10 to 10 items
                if self.queue.qsize() % 10 == 0:
                    print(f'Remaining: {self.queue.qsize()}')
                # trying to make a post request to susep page with the process number
                try:
                    susep_page = requests.post('https://www2.susep.gov.br/safe/menumercado/REP2/Produto.aspx/Consultar', { 'numeroProcesso' : number })
                except:
                    error = f'Query error in process {number}'
                    print(error)
                    self.process_errors.append({'numeroprocesso': number, 'msg': error})
                    continue
                # parsing the html page response to a beautiful soup object
                soup = BeautifulSoup(susep_page.text, 'html.parser')
                # trying to create a pdf link from the beautiful soup parser and after the name for the file
                try:
                    pdf_link = f'https://www2.susep.gov.br{soup.a["onclick"][15:-1]}'
                    
                    pdf_name = f'{str(number).replace("/", "-")}.pdf'
                except:
                    error = f'PDF Link construction error in process {number}'
                    print(error)
                    self.process_errors.append({'numeroprocesso': number, 'msg': error})
                    continue

                # trying to download the pdf file 
                try:
                    pdf = requests.get(pdf_link)
                except:
                    error = f'PDF error in process {number}'
                    print(error)
                    self.process_errors.append({'numeroprocesso':number, 'msg': error})
                    continue
                # writing the downloaded pdf to a file
                with open(pdf_name, 'wb') as output:
                    output.write(pdf.content)
                # calling pdf extractor to work on the pdf file and extract info
                PdfExtractor.main(pdf_name, self.outputJSON, number)
            # when the queue is empty release the lock and return the thread
            else:
                self.queueLock.release()
                return