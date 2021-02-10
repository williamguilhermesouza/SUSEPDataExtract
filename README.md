## SUSEP Data Extraction functions
![GitHub](https://img.shields.io/github/license/williamguilhermesouza/SUSEPDataExtract)
![Repo-size](https://img.shields.io/github/repo-size/williamguilhermesouza/SUSEPDataExtract)
![Last-commit](https://img.shields.io/github/last-commit/williamguilhermesouza/SUSEPDataExtract)

This repository was made as part of the [Carteira Global](https://github.com/carteiraglobal) technical challenge.
The repository with the challenge specifications can be found [here](https://github.com/carteiraglobal/challenge/tree/master/backend).

### Objective

The objectives of the challenge consisted of four main items:
- Extract and format the data from SUSEP [json](http://www.susep.gov.br/menu/consulta-de-produtos-1)
- Download and save all documents from the query in SUSEP site: http://www.susep.gov.br/menu/consulta-de-produtos-1
- Extract interest data from the documents downloaded
- Save the extracted data to an output JSON

### Business Logic

The work done is splitted between three python files:

#### main.py
The main file used as the application entrypoint. The logic inside this file consists of the data gathering and filtering from SUSEP, and then 
the creation and control of the threads that do the workout of downloading the pdfs and extracting data from them. Finally, the program outputs
the errors and the data extracted in two different JSONs.

#### PdfProcessing.py
This file holds a subclass of the Thread class, so it can be used as many threads objects. The PdfProcessing is responsible for the download of
the Pdf files and for calling the last file, to extract the data from the pdfs.

#### PdfExtractor.py
The PdfExtractor holds the logic behind the extraction of information in the downloaded pdf files. It passes the data extracted back to the main
file, so it can output it in the saved json.

#### PdfOCRParser.py
This class is used to parse pdf image files, as the ones scanned, into text. It is only enabled when the program is executed with the 'ocr' flag. The class is not used as standard because parsing the files to text with ocr takes too long, and then it would make the execution much slower. 

### How to use

The project uses [pipenv](https://pypi.org/project/pipenv/) project management. So, to run the project you must install pipenv with the command:

`pip install pipenv`

After installing pipenv simple run:

`pipenv install`

to install dependencies.

And then run the main file with:

`pipenv run python main.py`