CREATE TABLE IF NOT EXISTS empresas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj INTEGER NOT NULL,
    situacao TEXT NOT NULL,
    tipo TEXT NOT NULL,
    razao_social TEXT NOT NULL,
    estado TEXT NOT NULL,
    municipio TEXT NOT NULL,
    endereco TEXT NOT NULL,
    natureza_juridica TEXT NOT NULL,
    porte TEXT NOT NULL,
    atividade_principal TEXT NOT NULL,
    telefone TEXT NOT NULL,
    numero_funcionarios INTERGER,
    faturamento_anual_estimado INTERGER,
    vendedor_responsavel TEXT
);