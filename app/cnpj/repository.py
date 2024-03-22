from ..infra.database.database import get_db

def list_companys(vendedor):
    db = get_db()
    cursor = db.cursor()
    result = None
    if vendedor:
        result = cursor.execute("SELECT * FROM empresas WHERE vendedor_responsavel = ?", (vendedor,))
    else:
        result = cursor.execute("SELECT * FROM empresas")
    rows = cursor.fetchall()
    db.close()

    empresas = []
    
    for row in rows:
        empresa = {'id':row[0], 'cnpj':row[1], 'situacao':row[2], 'tipo':row[3], 'razao_social':row[4], 'estado':row[5], 'municipio':row[6], 'endereco':row[7], 'natureza_juridica':row[8], 'porte':row[9], 'atividade_principal':row[10], 'telefone':row[11], 'numero_funcionarios':row[12], 'faturamento_anual_estimado':row[13], 'vendedor_responsavel':row[14]}
        empresas.append(empresa)
    return empresas

def create(data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO empresas (cnpj, situacao, tipo, razao_social, estado, municipio, endereco, natureza_juridica, porte, atividade_principal, telefone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    db.commit()
    db.close()
    return "OK"

def update(data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE empresas SET numero_funcionarios = ?, faturamento_anual_estimado = ?, vendedor_responsavel = ? WHERE id = ?", data)
    db.commit()
    db.close()
    return "OK"