#Requisitos
Antes de começar a executar o projeto, verifique se você tem os seguintes requisitos instalados em sua máquina:

Python 3.x

#Instalação
Para instalar as dependências necessárias para o projeto, execute o seguinte comando no terminal:

pip install -r requirements.txt

Este comando instalará todas as bibliotecas Python necessárias para o projeto.

#Configuração do Banco de Dados
O projeto utiliza um banco de dados SQLite. Para configurar o banco de dados com as tabelas necessárias, execute o seguinte comando no terminal:

python database.py

Este comando criará o arquivo de banco de dados database.db e configurará as tabelas necessárias conforme especificado no arquivo schema.sql.

#Utilização
Para iniciar o servidor Flask e executar o projeto, utilize o seguinte comando no terminal:

python manager.py

Após executar este comando, a API REST será ativada e estará pronta para receber solicitações. O servidor será iniciado em http://127.0.0.1:8080/ por padrão.

#Endpoints
O projeto disponibiliza os seguintes endpoints:

GET /cnpj: Lista informações sobre empresas. Parâmetros opcionais: vendedor_responsavel para filtrar por vendedor.
POST /cnpj: Cria uma nova entrada de empresa. Requer um payload JSON com o campo cnpj.
PUT /cnpj/<id>: Atualiza informações de uma empresa. Requer um payload JSON com os campos numero_funcionarios, faturamento_anual_estimado e vendedor_responsavel.

Certifique-se de usar os métodos HTTP corretos ao acessar os endpoints.