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

def main(pdf_name):
    with open(pdf_name, 'rb') as inputfile:
        pdfReader = PyPDF2.PdfFileReader(inputfile)
        try:
            numPages = pdfReader.getNumPages()

            search_table_bool = False

            for page_number in range(numPages):
                page_text = pdfReader.getPage(page_number).extractText()

                search_cnpj = page_text.find('CNPJ de n')
                if search_cnpj != -1:
                    cnpj = page_text[search_cnpj+11 : search_cnpj+32].replace('\n','')
                    print(cnpj)

                search_entity_name = page_text.find('Art. 1°')
                if search_entity_name != -1:
                    entity_name_comma = page_text.find(',')
                    entity_name = page_text[search_entity_name+12:entity_name_comma]
                    print(entity_name)

                search_description = page_text.find('institui o')
                if search_description != -1:
                    description_comma = page_text.find(',',search_description)
                    description_second_comma = page_text.find(',', description_comma+11)
                    description = page_text[search_description+11:description_second_comma].replace('\n','')
                    print(description)

                search_table = page_text.find('tábuas biométricas de sobrevivência')
                if search_table != -1 and not search_table_bool:
                    search_table_bool = True
                    search_male = page_text.find('masculino', search_table)
                    search_female = page_text.find('feminino', search_table)
                    male = page_text[search_male+10:search_male+18].replace('\n','')
                    female = page_text[search_female+9:search_female+16].replace('\n','')
                    print(male, female)

                search_charge = page_text.find('cobrará carregamento')
                if search_charge != -1:
                    percent = page_text.find('%', search_charge)
                    charge = page_text[percent - 2:percent+1] 
                    print(charge)
        except:
            print('error extracting pdf')



if __name__ == '__main__':
    main('001-00210-89.pdf')