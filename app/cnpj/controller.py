from flask import Blueprint, app, jsonify, make_response, request
from .service import list_cnpj, create_cnpj, change_cnpj

empresa = Blueprint('empresa', __name__, template_folder='templates')
@empresa.route('/<page>')

@empresa.route('/cnpj', methods=['GET'])

def list():
    vendedor = request.args.get('vendedor_responsavel')
    result = list_cnpj(vendedor)
    return jsonify(result)

@empresa.route('/cnpj', methods=['POST'])
def create():
    data = request.json
    if 'cnpj' not in data:
        return make_response('cnpj não inserido.', 400)
    if not data['cnpj']:
        return make_response('cnpj vazio.', 400)
    if len(str(data['cnpj'])) != 14 or not isinstance(data['cnpj'], int):
        return make_response('Por favor, insira um cnpj válido.', 400)
    result = create_cnpj(data['cnpj'])
    return jsonify(result)

@empresa.route('/cnpj/<id>', methods=['PUT'])

def change(id):
    data = request.json

    if 'numero_funcionarios' not in data:
        return make_response('numero_funcionarios não inserido.', 400)
    if not isinstance(data['numero_funcionarios'], int):
        return make_response('numero_funcionarios precisa ser um inteiro..', 400)
    
    if 'faturamento_anual_estimado' not in data:
        return make_response('faturamento_anual_estimado não inserido.', 400)
    if not isinstance(data['faturamento_anual_estimado'], int):
        return make_response('faturamento_anual_estimado precisa ser um inteiro.', 400)
    
    if 'vendedor_responsavel' not in data:
        return make_response('vendedor_responsavel não inserido.', 400)
    if not isinstance(data['vendedor_responsavel'], str):
        return make_response('vendedor_responsavel precisa ser uma string.', 400)
    if not len(data['vendedor_responsavel']):
        return make_response('vendedor_responsavel vazio.', 400)
    
    
    data['id'] = id
    return change_cnpj(data)