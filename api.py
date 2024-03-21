from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def formatar_cnpj(cnpj):
    if len(cnpj) != 14:
        return 'CNPJ inválido'
    
    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'

@app.route('/consulta_cnpj', methods=['GET'])
def consulta_cnpj():
    cnpj = request.args.get('cnpj')
    
    if not cnpj:
        return jsonify({'error': 'CNPJ não fornecido'}), 400
    
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Falha na consulta da Receita Federal'}), 500
    
    data = response.json()
    
    empresa = {
        'CNPJ': data['cnpj'],
        'Situacao': data['situacao'],
        'Tipo': data['tipo'],
        'Razao Social': data['nome'],
        'Nome Fantasia': data['fantasia'],
        'Estado': data['uf'],
        'Municipio': data['municipio'],
        'Endereco': data['logradouro'] + ', ' + data['numero'],
        'Natureza Juridica': data['natureza_juridica'],
        'Atividade Principal': data['atividade_principal'][0]['text'],
        'Telefone': data['telefone'],
        'Numero de Funcionários': None,
        'Faturamento Anual Estimado': None,
        'Vendedor Responsavel': None
    }
    
    cnpj_formatado = formatar_cnpj(cnpj)
    print(f'CNPJ consultado: {cnpj_formatado}')
    
    return jsonify(empresa), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
