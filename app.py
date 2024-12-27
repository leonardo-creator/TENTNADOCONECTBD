from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

# Criação da aplicação Flask
app = Flask(__name__)

# Função para conectar ao banco de dados
def connect_db():
    try:
        return psycopg2.connect(
            host="singly-light-topi.data-1.use1.tembo.io",  # Substitua pelo seu host
            database="pecas",  # Substitua pelo seu banco de dados
            user="postgres",  # Substitua pelo seu usuário
            password="7sw0F2MNx0ObN32g",  # Substitua pela sua senha
            port=5432  # Porta padrão do PostgreSQL
        )
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Rota para retornar todos os dados
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Conectando ao banco
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Falha ao conectar ao banco de dados"}), 500
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Consulta para buscar todos os dados (substitua 'sua_tabela' pelo nome da tabela)
        cursor.execute("SELECT * FROM pecas")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Retorna os dados em formato JSON
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para verificar se a API está ativa
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API está funcionando!"}), 200

# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

