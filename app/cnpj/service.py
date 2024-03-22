import requests
from .repository import list_companys, create, update

#listar cnpj
def list_cnpj(vendedor):
    return list_companys(vendedor)
#criar cnpj
def create_cnpj(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)
    if response.status_code == 200:
        consulta_cnpj = response.json()
        empresa = (cnpj, consulta_cnpj['situacao'], consulta_cnpj['tipo'], consulta_cnpj['nome'], consulta_cnpj['uf'], consulta_cnpj['municipio'], consulta_cnpj['logradouro'], consulta_cnpj['natureza_juridica'], consulta_cnpj['porte'], consulta_cnpj['atividade_principal'][0]['text'], consulta_cnpj['telefone'])

        print(consulta_cnpj)
        return create(empresa)
#atualizar cnpj
def change_cnpj(data):
    empresa = (data['numero_funcionarios'], data['faturamento_anual_estimado'], data['vendedor_responsavel'], data['id'])
    return update(empresa)