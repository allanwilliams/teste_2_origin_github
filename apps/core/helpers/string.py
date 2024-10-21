from io import StringIO
from html.parser import HTMLParser
import re

def is_cpf(cpf):
    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números:
    if len(numbers) != 11:
        return False

    # Verifica se todos os números são repetidos
    if len(list(dict.fromkeys(numbers))) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def valida_cpf(cpf):
    regex_cpf = re.compile(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$')
    return re.match(regex_cpf, cpf)

def valida_cnpj(cnpj):
    regex_cnpj = re.compile(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$')
    return re.match(regex_cnpj, cnpj)

def valida_cpf_cnpj(cpf_cnpj):
    cpf_cnpj_clean = re.sub('[^0-9]', '', cpf_cnpj)
    regex_cpf_cnpj = re.compile(r'(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)|(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)')
    is_cpf_cnpj_valido_regex = re.match(regex_cpf_cnpj, cpf_cnpj)
    return is_cpf_cnpj_valido_regex or len(cpf_cnpj_clean) in [11, 14]

def valida_num_processo(num_processo):
    num_processo_clean = re.sub('[^0-9]', '', num_processo)
    regex_num_processo = re.compile(r'^\d{7}\-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$')
    is_num_processo_valido_regex = re.match(regex_num_processo, num_processo)

    return is_num_processo_valido_regex or len(num_processo_clean) == 20

def valida_num_protocolo(num_protocolo):
    regex_num_protocolo = re.compile(r'^\d{8}\/\d{4}$')
    return re.match(regex_num_protocolo, num_protocolo)