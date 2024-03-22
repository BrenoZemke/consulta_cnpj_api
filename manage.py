from flask import Flask, request, jsonify
from app.infra.database.database import init_db
from app.cnpj.controller import empresa

app = Flask(__name__)
app.register_blueprint(empresa)
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='127.0.0.1', port=8080, debug=True)
    