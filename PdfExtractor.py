import PyPDF2

'''
Extract from the PDFs:
{
    process_number: 15414.900943/2013-72,
    entity_cnpj: 51.990.695/0001-37,
    entity_name:  BRADESCO VIDA E PREVIDÊNCIA S.A.,
    process_description: VGBL INDIVIDUAL - Renda fixa,
    distribution_date: 14/10/2013,
    male_atuarial_table: BR-EMSsb,
    female_atuarial_table:  BR-EMSsb,
    loading_tax: 0% Cobrado quando da efetivação de pedidos de resgate e/ou portabilidade ,
    interest_tax: 0%
    reversion_percentual: 0%,
    SUSEP_status: ARQUIVADO/ARQUIVO GERAL,
    lone_payment:  SIM,
    temporary_monthly: SIM
    certain_monthly_deadline: SIM
    lifelong_monthly: SIM
    Mensal vitalícia com prazo mínimo garantido: SIM
    Mensal vitalícia reversível ao beneficiário indicado: SIM
    Mensal vitalícia reversível ao cônjuge com continuidade aos menores (maioridade aos 24): SIM
    Mensal vitalícia reversível ao cônjuge: N/A
    Mensal reversível aos menores: N/A

    Da aplicação dos recursos
    (Art. 54. Os recursos do plano serão aplicados em um dos seguintes FIEs)

    CNPJ Fundo | Nome Fundo | Taxa de Administração
    17.488.983/0001-50 BRADESCO FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO RENDA FIXA I-A 1,9 %
    17.488.691/0001-17 BRADESCO FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO RENDA FIXA II-A 1,9 %
    17.517.216/0001-21 BRADESCO FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO RENDA FIXA III-A 1,5 %
    17.517.250/0001-04 BRADESCO FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO RENDA FIXA IV-A 1,2 %
    17.517.268/0001-06 BRADESCO FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO RENDA FIXA V-A 1 %
    17.999.961/0001-54 BRADESCO FUNDO DE INVESTIMENTO RENDA FIXA MÁSTER IV PREVIDÊNCIA 0 %

    Parâmetros técnicos
    Valor mínimo da provisão matemática de benefícios a conceder: R$ 500,00
    Prazo de Carência: 6 meses
    Carência para Portabilidade: 60 dias
    Carência para Portabilidade na própria Entidade: 60 dias
}
'''

def main(pdf_name, outputJSON, process_number):
    with open(pdf_name, 'rb') as inputfile:
        pdfReader = PyPDF2.PdfFileReader(inputfile)
        try:
            numPages = pdfReader.getNumPages()

            search_table_bool = False
            lone_payment = temporary_monthly = certain_monthly = lifelong_monthly = granted_monthly = indicated_reversible = \
                partner_minor_age_reversible = partner_reversible = minor_age_reversible = 'N/A'

            for page_number in range(numPages):
                page_text = pdfReader.getPage(page_number).extractText()

                #process_number

                search_cnpj = page_text.find('CNPJ de n')
                if search_cnpj != -1:
                    cnpj = page_text[search_cnpj+11 : search_cnpj+32].replace('\n','')

                search_entity_name = page_text.find('Art. 1°')
                if search_entity_name != -1:
                    entity_name_comma = page_text.find(',')
                    entity_name = page_text[search_entity_name+12:entity_name_comma]

                search_description = page_text.find('institui o')
                if search_description != -1:
                    description_comma = page_text.find(',',search_description)
                    description_second_comma = page_text.find(',', description_comma+11)
                    description = page_text[search_description+11:description_second_comma].replace('\n','')

                distribution_date = '14/10/2013'

                search_table = page_text.find('tábuas biométricas de sobrevivência')
                if search_table != -1 and not search_table_bool:
                    search_table_bool = True
                    search_male = page_text.find('masculino', search_table)
                    search_female = page_text.find('feminino', search_table)
                    male = page_text[search_male+10:search_male+18].replace('\n','')
                    female = page_text[search_female+9:search_female+16].replace('\n','')

                search_charge = page_text.find('cobrará carregamento')
                if search_charge != -1:
                    percent = page_text.find('%', search_charge)
                    loading_tax = page_text[percent - 2:percent+1] 

                search_interest = page_text.find('taxa de juros efetiva anual')
                if search_interest != -1:
                    percent = page_text.find('%', search_interest)
                    if percent != -1:
                        interest_tax = page_text[search_interest+28:percent+1]

                # reversion_percent
                # susep_status

                search_lone = page_text.find('pagamento único')
                if search_lone != -1:
                    lone_payment = 'SIM'

                search_monthly = page_text.find('mensal temporária')
                if search_monthly != -1:
                    temporary_monthly = 'SIM'
 
                search_certain = page_text.find('prazo certo')
                if search_certain != -1:
                    certain_monthly = 'SIM'

                search_lifelong = page_text.find('mensal vitalícia')
                if search_lifelong != -1:
                    lifelong_monthly = 'SIM'

                search_minimum = page_text.find('vitalícia com prazo mínimo')
                if search_minimum != -1:
                    granted_monthly = 'SIM'

                search_reversible = page_text.find('vitalícia reversível ao beneficiário')
                if search_reversible != -1:
                    indicated_reversible = 'SIM'

                search_partner_minor = page_text.find('vitalícia reversível ao cônjuge com continuidade aos menores')
                if search_partner_minor != -1:
                    partner_minor_age_reversible = 'SIM'

                search_partner = page_text.find('vitalícia reversível ao cônjuge:')
                if search_partner != -1:
                    partner_reversible = 'SIM'

                search_minor_reversible = page_text.find('reversível aos menores')
                if search_minor_reversible != -1:
                    minor_age_reversible = 'SIM'
                
                #DA APLICAÇÃO DOS RECURSOS

                minimum_value_search = page_text.find('se o saldo for inferior a')
                minimum_value = ""
                if minimum_value_search != -1:
                    minimum_value = page_text[minimum_value_search+30:minimum_value_search+36]
                
                grace_period_search = page_text.find('resgate')
                grace_period = ""
                if grace_period_search != -1:
                    grace_search = page_text.find('prazo de carência', grace_period_search)
                    grace_comma = page_text.find(',',grace_search)
                    if grace_search != -1 and grace_comma != -1:
                        grace_period = page_text[grace_search+17:grace_comma]

                search_portable_deadline = page_text.find('portabilidade')
                portable_deadline = ""
                if search_portable_deadline != -1:
                    portable_search = page_text.find('prazo de carência', search_portable_deadline)
                    portable_comma = page_text.find(',', portable_search)
                    if portable_search != -1 and portable_comma != -1:
                        portable_deadline = page_text[portable_search+17:portable_comma]

                #propria entidade

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
                "reversion_percent": "",
                "SUSEP_status": "",
                "lone_payment": lone_payment,
                "temporary_monthly": temporary_monthly,
                "certain_monthly": certain_monthly,
                "lifelong_monthly": lifelong_monthly,
                "lifelong_monthly_with_granted_minimum_deadline": granted_monthly,
                "monthly_reversible_indicated": indicated_reversible,
                "monthly_reversible_to_partner_with_minors_continuation": partner_minor_age_reversible,
                "monthly_partner_reversible": partner_reversible,
                "monthly_minor_age_reversible": minor_age_reversible,
                "resources_application": "",
                "minimum_value": minimum_value,
                "grace_period": grace_period,
                "portability_grace_period": portable_deadline,
                "portability_grace_period_own_entity": "",
            })

            print(outputJSON)

        except:
            print('error extracting pdf')



if __name__ == '__main__':
    output = []
    main('001-00210-89.pdf', output, '001-00210-89')