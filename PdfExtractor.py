import PyPDF2
import re

## This function is responsible for the extraction of informations from the pdfs
# it parses all the pdf pages and looks for especific patterns and substrings
# that matches the data that needs to be extracted
# This function may be improved using the pytesseract lib to extract information
# from image pdfs too
def main(pdf_name, outputJSON, process_number):

    # defining the placeholder variables that will be passed as a dictionary outside the function
    search_table_bool = False
    lone_payment = temporary_monthly = certain_monthly = lifelong_monthly = granted_monthly = indicated_reversible = \
        partner_minor_age_reversible = partner_reversible = minor_age_reversible = 'N/A'
    
    cnpj = entity_name = description = distribution_date = male = female = loading_tax = interest_tax = reversion_percent = \
        susep_status = resources_application = minimum_value = grace_period = portable_deadline = portable_own_deadline = ''

    # defining the Regex expressions
    cnpj_pattern = re.compile(r"[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}")


    # opening the pdf file in byte mode and parsing it with pypdf2
    with open(pdf_name, 'rb') as inputfile:
        pdfReader = PyPDF2.PdfFileReader(inputfile)

        # trying to get description from document title
        description = pdfReader.getDocumentInfo().title

        # try block with main logic, gets the number of pages then iterates through them
        try:
            numPages = pdfReader.getNumPages()

            for page_number in range(numPages):
                # extracting text from pdf, and parsing to useful formats
                page_text = pdfReader.getPage(page_number).extractText()

                page_text_nolinebreak = page_text.replace('\n', '')
                
                page_text_lowercase = page_text.lower()

                # using Regex to extract CNPJ
                cnpj_search = cnpj_pattern.search(page_text_nolinebreak)
                if cnpj_search: 
                    cnpj = cnpj_search.group(0)
                

                # using find to extract entity_name
                search_entity_name = page_text.find('Art. 1°')
                if search_entity_name != -1:
                    entity_name_comma = page_text.find(',')
                    entity_name = page_text[search_entity_name+12:entity_name_comma]

                # checking the document title for description, if there is no title try to scrape
                # description
                if description == '' or description == None:
                    search_description = page_text.find('institui o')
                    if search_description != -1:
                        description_comma = page_text.find(',',search_description)
                        description_second_comma = page_text.find(',', description_comma+11)
                        description = page_text[search_description+11:description_second_comma].replace('\n','')

                #TODO distribution date
                distribution_date = ''

                # trying to find atuarial table, and then extracting the info
                search_table = page_text.find('tábuas biométricas de sobrevivência')
                if search_table != -1 and not search_table_bool:
                    search_table_bool = True
                    search_male = page_text.find('masculino', search_table) + 11
                    search_female = page_text.find('feminino', search_table) + 10
                    search_male_space = page_text.find(' ', search_male)
                    search_female_space = page_text.find(' ', search_female)
                    male = page_text[search_male:search_male_space].replace('\n','')
                    female = page_text[search_female:search_female_space].replace('\n','')
                    print(search_male, search_male_space)

                # trying to extract loading tax
                search_charge = page_text.find('cobrará carregamento')
                if search_charge != -1:
                    percent = page_text.find('%', search_charge)
                    loading_tax = page_text[percent - 2:percent+1] 

                # trying to extract interest tax
                search_interest = page_text.find('taxa de juros efetiva anual')
                if search_interest != -1:
                    percent = page_text.find('%', search_interest)
                    if percent != -1:
                        interest_tax = page_text[search_interest+28:percent+1]

                # trying to extract reversion tax
                search_reversion = page_text.find('percentual de reversão')
                reversion_percent = '0%'
                if search_reversion != -1:
                    percent = page_text.find('%', search_reversion)
                    if percent != -1:
                        reversion_percent = page_text[search_reversion+23:percent+1]
                
                #TODO susep status comes from download page
                susep_status = ''

                # YES / NO block , if the info is found within the document flag it as 
                # yes and else no
                search_lone = page_text_lowercase.find('pagamento único')
                if search_lone != -1:
                    lone_payment = 'SIM'

                search_monthly = page_text_lowercase.find('mensal temporária')
                if search_monthly != -1:
                    temporary_monthly = 'SIM'
 
                search_certain = page_text_lowercase.find('prazo certo')
                if search_certain != -1:
                    certain_monthly = 'SIM'

                search_lifelong = page_text_lowercase.find('mensal vitalícia')
                if search_lifelong != -1:
                    lifelong_monthly = 'SIM'

                search_minimum = page_text_lowercase.find('vitalícia com prazo mínimo')
                if search_minimum != -1:
                    granted_monthly = 'SIM'

                search_reversible = page_text_lowercase.find('vitalícia reversível ao beneficiário')
                if search_reversible != -1:
                    indicated_reversible = 'SIM'

                search_partner_minor = page_text_lowercase.find('vitalícia reversível ao cônjuge com continuidade aos menores')
                if search_partner_minor != -1:
                    partner_minor_age_reversible = 'SIM'

                search_partner = page_text_lowercase.find('vitalícia reversível ao cônjuge:')
                if search_partner != -1:
                    partner_reversible = 'SIM'

                search_minor_reversible = page_text_lowercase.find('reversível aos menores')
                if search_minor_reversible != -1:
                    minor_age_reversible = 'SIM'
                
                #TODO resources application must be extracted with regex
                resources_application = ''

                # trying to extract minimum value 
                minimum_value_search = page_text.find('se o saldo for inferior a')
                if minimum_value_search != -1:
                    minimum_value = page_text[minimum_value_search+30:minimum_value_search+36]
                
                #trying to extract grace period
                grace_period_search = page_text.find('resgate')
                if grace_period_search != -1:
                    grace_search = page_text.find('prazo de carência', grace_period_search)
                    grace_comma = page_text.find(',',grace_search)
                    if grace_search != -1 and grace_comma != -1:
                        grace_period = page_text[grace_search+17:grace_comma]

                # trying to extract portable deadline
                search_portable_deadline = page_text.find('portabilidade')
                if search_portable_deadline != -1:
                    portable_search = page_text.find('prazo de carência', search_portable_deadline)
                    portable_comma = page_text.find(',', portable_search)
                    if portable_search != -1 and portable_comma != -1:
                        portable_deadline = page_text[portable_search+17:portable_comma]

                #TODO own entity portabledeadline

            # appending scraped info to given list
            outputJSON.append({
                "process_number": process_number,
                "entity_cnpj": cnpj,
                "entity_name": entity_name,
                "process_description": description,
                "distribution_date": distribution_date,
                "male_atuarial_table": male,
                "female_atuarial_table": female,
                "loading_tax": loading_tax,
                "interest_tax": interest_tax,
                "reversion_percent": reversion_percent,
                "SUSEP_status": susep_status,
                "lone_payment": lone_payment,
                "temporary_monthly": temporary_monthly,
                "certain_monthly": certain_monthly,
                "lifelong_monthly": lifelong_monthly,
                "lifelong_monthly_with_granted_minimum_deadline": granted_monthly,
                "monthly_reversible_indicated": indicated_reversible,
                "monthly_reversible_to_partner_with_minors_continuation": partner_minor_age_reversible,
                "monthly_partner_reversible": partner_reversible,
                "monthly_minor_age_reversible": minor_age_reversible,
                "resources_application": resources_application,
                "minimum_value": minimum_value,
                "grace_period": grace_period,
                "portability_grace_period": portable_deadline,
                "portability_grace_period_own_entity": portable_own_deadline
            })

        # except block to prevent function from failing 
        except:
            print('Error extracting pdf')


# local tests
if __name__ == '__main__':
    output = []
    main('001-00210-89.pdf', output, '001-00210-89')
    main('15414.900943-2013-72.pdf', output, '15414.900943-2013-72')

    for process in output:
        print(process)
        print('\n')

