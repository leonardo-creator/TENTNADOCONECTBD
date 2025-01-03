from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuração do banco de dados
DB_CONN = "postgresql://postgres:7sw0F2MNx0ObN32g@singly-light-topi.data-1.use1.tembo.io:5432/postgres"

# Inicializando o aplicativo Flask
app = Flask(__name__)

@app.route("/dados", methods=["GET"])
def get_dados():
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(DB_CONN)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Executar a query para obter os dados
        query = """
        SELECT 
            barragem AS barragem,
            "Data e Hora" AS data_e_hora,
            "Nível (m)" AS nivel_m,
            "Volume (mm)" AS volume_mm
        FROM dados_barragens
        """
        cursor.execute(query)
        dados = cursor.fetchall()

        # Fechar conexão
        cursor.close()
        conn.close()

        # Retornar os dados como JSON
        return jsonify(dados), 200

    except Exception as e:
        # Retornar erro em caso de falha
        return jsonify({"error": f"Erro ao obter dados: {e}"}), 500

# Configuração do servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
